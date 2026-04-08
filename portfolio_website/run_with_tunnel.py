from pyngrok import ngrok
import subprocess
import sys

port = 8000
print('Starting ngrok tunnel for http://localhost:%s' % port)
public_url = ngrok.connect(port, bind_tls=True).public_url
print('Public URL:', public_url)
print('Starting FastAPI server...')
subprocess.run([sys.executable, '-m', 'uvicorn', 'main:app', '--host', '0.0.0.0', '--port', str(port), '--reload'])
