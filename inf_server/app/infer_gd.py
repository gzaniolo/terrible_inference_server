import ast
from argparse import ArgumentParser

import sys

sys.path.append('/mmdetection')

# from mmengine.logging import print_log

from mmdet.apis import DetInferencer
from mmdet.evaluation import get_classes
from mmdet.models.detectors.glip import run_ner

import os


# Generate args in a way that is similar to the demo scripts; don't want to 
#  accidentally mess up any defaults
def parse_args(
    inputs,
    model,
    weights=None,
    out_dir='outputs',
    texts=None,
    device='cuda:0',
    pred_score_thr=0.3,
    batch_size=1,
    show=False,
    no_save_vis=False,
    no_save_pred=False,
    print_result=False,
    palette='none',
    custom_entities=False,
    chunked_size=-1,
    tokens_positive=None
):
    # Construct call_args from input arguments
    call_args = {
        'inputs': inputs,
        'model': model,
        'weights': weights,
        'out_dir': out_dir,
        'texts': texts,
        'device': device,
        'pred_score_thr': pred_score_thr,
        'batch_size': batch_size,
        'show': show,
        'no_save_vis': no_save_vis,
        'no_save_pred': no_save_pred,
        'print_result': print_result,
        'palette': palette,
        'custom_entities': custom_entities,
        'chunked_size': chunked_size,
        'tokens_positive': tokens_positive
    }

    # Adjust call_args based on conditional logic
    if call_args['no_save_vis'] and call_args['no_save_pred']:
        call_args['out_dir'] = ''

    if call_args['model'].endswith('.pth'):
        print('The model is a weight file, automatically '
              'assigning the model to --weights')
        call_args['weights'] = call_args['model']
        call_args['model'] = None

    if call_args['texts'] is not None:
        if call_args['texts'].startswith('$:'):
            dataset_name = call_args['texts'][3:].strip()
            class_names = get_classes(dataset_name)
            call_args['texts'] = [tuple(class_names)]

    if call_args['tokens_positive'] is not None:
        call_args['tokens_positive'] = ast.literal_eval(call_args['tokens_positive'])

    # Extract init_args from call_args
    init_kws = ['model', 'weights', 'device', 'palette']
    init_args = {kw: call_args.pop(kw) for kw in init_kws}

    return init_args, call_args

# Don't actually use some of the call args when we call
pathname = f"img_file{os.getpid()}.jpg"

# # Stock config:
# init_args, call_args = parse_args(
#     inputs='../../mmdetection/demo/demo.jpg',
#     model='../../mmdetection/configs/grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_cap4m.py',
#     weights='../../mmdetection/groundingdino_swint_ogc_mmdet-822d7e9d.pth',
#     texts='bench . car .',
#     no_save_pred=True,
#     no_save_vis=True)
# Coco config:
init_args, call_args = parse_args(
    inputs=pathname,
    model='../../mmdetection/configs/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365.py',
    weights='../../mmdetection/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth',
    texts='$: coco',
    # no_save_pred=False,
    # no_save_vis=False)
    no_save_pred=True,
    no_save_vis=True)

inferencer = DetInferencer(**init_args)

chunked_size = call_args.pop('chunked_size')
inferencer.model.test_cfg.chunked_size = chunked_size

def handle_img(img_path, texts):
    
    global call_args
    call_args['texts'] = texts

    out_dic = inferencer(**call_args)
    # Seems flakey and possibly wrong. Double check...
    tokens_positive, noun_phrases = run_ner(texts)

    # # # Many print statements re-activate if useful
    # print("CLASSES AAAAAAAAAAAAA")
    # print(noun_phrases)
    # print("BBBBBB")
    # print(texts)
    # print("AAAAAAAAAAA")

    # return out_dic
    return out_dic, noun_phrases