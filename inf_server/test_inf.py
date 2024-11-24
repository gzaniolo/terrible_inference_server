import ast
from argparse import ArgumentParser

import sys

sys.path.append('/mmdetection')

from mmengine.logging import print_log

from mmdet.apis import DetInferencer
from mmdet.evaluation import get_classes




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

# Example function usage:
# init_args, call_args = parse_args(
#     inputs="image.jpg",
#     model="model_config.pth",
#     texts="$: coco",
#     tokens_positive="[[1,2],[3,4]]"
# )


if __name__ == "__main__":
    init_args, call_args = parse_args(
        inputs='../../mmdetection/demo/demo.jpg',
        model='../../mmdetection/configs/grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_cap4m.py',
        weights='../../mmdetection/groundingdino_swint_ogc_mmdet-822d7e9d.pth',
        texts='bench . car .',
        no_save_pred=True,
        no_save_vis=True)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
    print(init_args)
    print(call_args)
    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")

    # desired
    # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    # {'model': 'configs/grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_cap4m.py', 
    #  'weights': 'groundingdino_swint_ogc_mmdet-822d7e9d.pth', 
    #  'device': 'cuda:0', 
    #  'palette': 'none'}
    # 
    # {'inputs': 'demo/demo.jpg', 
    #  'out_dir': 'outputs', 
    #  'texts': 'bench . car .', 
    #  'pred_score_thr': 0.3, 
    #  'batch_size': 1, 
    #  'show': False, 
    #  'no_save_vis': False, 
    #  'no_save_pred': False, 
    #  'print_result': False, 
    #  'custom_entities': False, 
    #  'chunked_size': -1, 
    #  'tokens_positive': None}
    # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
    # mine:



    inferencer = DetInferencer(**init_args)

    chunked_size = call_args.pop('chunked_size')
    inferencer.model.test_cfg.chunked_size = chunked_size

    out_dic = inferencer(**call_args)

    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")
    print(out_dic)
    print("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB")

    if call_args['out_dir'] != '' and not (call_args['no_save_vis']
                                           and call_args['no_save_pred']):
        print_log(f'results have been saved at {call_args["out_dir"]}')

# image file 'inputs'
# 'model' 'configs/grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_cap4m.py'
# 'weights' 'groundingdino_swint_ogc_mmdet-822d7e9d.pth'
# 'texts' 'bench . car .'

# python demo/image_demo.py 
# demo/demo.jpg 
# configs/grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_cap4m.py 
# --weights groundingdino_swint_ogc_mmdet-822d7e9d.pth 
# --texts 'bench . car .'