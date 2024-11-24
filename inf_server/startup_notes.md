# Notes for startup

From directory outside of this one:
```
docker build -f Dockerfile_inf_server -t inf_server
```

In this directory (important!!!):
```
docker run -v $(pwd)/:/webserver -p 4000:80 -it --entrypoint /bin/bash --gpus all --name inf_server inf_server
```

Convenient copy paste
```
nginx
service nginx status 
docker restart myapp-dbg
docker exec -it myapp-dbg /bin/bash 
gunicorn -c gunicorn.conf.py --workers 1 --bind 0.0.0.0:8000 myapp:app
```


<!-- aa -->
### additional things:
added to dockerfile
```
cd /mmdetection
apt install wget
wget https://download.openmmlab.com/mmdetection/v3.0/grounding_dino/groundingdino_swint_ogc_mmdet-822d7e9d.pth
pip install transformers
pip install nltk
```
"From an interactive python shell"
```
import nltk
nltk.download('punkt', download_dir='/root/nltk_data')
nltk.download('averaged_perceptron_tagger', download_dir='/root/nltk_data')
```


demo run command
```
python demo/image_demo.py demo/demo.jpg configs/grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_cap4m.py --weights groundingdino_swint_ogc_mmdet-822d7e9d.pth --texts 'bench . car .'
```