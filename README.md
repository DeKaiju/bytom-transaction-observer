# bytom-transaction-observer
 
python version: python3  
usage: python observer.py [-h] -a A -c C [-i I]  
optional arguments:  
  -h, --help  show this help message and exit  
  -a A        wallet address  
  -c C        transaction confirmation  
  -i I        request interval  
```shell
pip install -r requirements.txt
python observer.py -a bm1q3yt265592czgh96r0uz63ta8fq40uzu5a8c2h0 -c 10 -i 60
```