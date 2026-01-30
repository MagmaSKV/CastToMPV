#!/usr/bin/env python3
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, unquote
import subprocess
import threading
import time
import argparse
import sys
import os
import socket
import shlex

class VideoHandler(BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.debug_mode = kwargs.pop('debug', False)
        self.title = kwargs.pop('title', 'Cast from {device}')
        self.app = kwargs.pop('app', 'mpv')
        self.app_args = kwargs.pop('app_args', '')
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("""
            <html><body style="font-family:Arial;padding:20px">
            <h1>🎬 PC Video Receiver</h1>
            <p>Status: <span style="color:green">✅ Active</span></p>
            <p>Ready to receive videos from mobile devices</p>
            </body></html>""".encode())
            if self.debug_mode:
                print(f"[DEBUG] GET / from {self.client_address[0]}")
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else ""
        
        if self.path == "/play":
            params = parse_qs(post_data)
            url = unquote(params.get('url', [''])[0])
            post_device = unquote(params.get('device', [''])[0])
            
            headers_device = self.headers.get('X-Device-Name', 'Unknown Device')
            device_model = self.headers.get('X-Device-Model', 'Unknown Model')
            
            device_name = headers_device if headers_device != 'Unknown Device' else post_device
            if not device_name:
                device_name = f"{device_model}"
            
            if url:
                timestamp = time.strftime("%H:%M:%S")
                if self.debug_mode:
                    print(f"\n{'─'*40}\n📱 VIDEO RECEIVED\n{'─'*40}")
                    print(f"⏰ {timestamp}\n📱 {device_name}")
                    print(f"🔗 {url[:70]}..." if len(url) > 70 else f"🔗 {url}")
                    print(f"{'─'*40}")
                
                self.send_response(200)
                self.send_header('Content-type', 'text/plain; charset=utf-8')
                self.end_headers()
                self.wfile.write(f"✅ Video received from {device_name}".encode())
                
                threading.Thread(target=self.play_video, args=(url, device_name), daemon=True).start()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No URL")
                
        elif self.path == "/test":
            headers_device = self.headers.get('X-Device-Name', 'Test Device')
            if self.debug_mode:
                print(f"\n{'─'*40}\n✅ TEST FROM {headers_device}\n{'─'*40}")
                print(f"📱 {headers_device}\n🌐 {self.client_address[0]}")
                print(f"⏰ {time.strftime('%H:%M:%S')}\n{'─'*40}")
            else:
                print(f"✅ Test from {headers_device} ({self.client_address[0]})")
            
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"✅ Test successful from {headers_device}".encode())
            
        elif self.path == "/testVideo":
            headers_device = self.headers.get('X-Device-Name', 'Test Device')
            if self.debug_mode:
                print(f"\n{'─'*50}\n🎥 TEST VIDEO FROM {headers_device}\n{'─'*50}")
                print(f"📱 {headers_device}\n🌐 {self.client_address[0]}")
                print(f"⏰ {time.strftime('%H:%M:%S')}\n🎥 test.mp4\n{'─'*50}")
            else:
                print(f"🎥 Video test from {headers_device} ({self.client_address[0]})")
            
            video_path = "file://" + os.path.join(os.getcwd(), "test.mp4")
            self.send_response(200)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write(video_path.encode())
            
            threading.Thread(target=self.play_video, args=(video_path, headers_device), daemon=True).start()
            
        else:
            self.send_response(404)
            self.end_headers()
    
    def play_video(self, url, device_name):
        try:            
            window_title = self.title.replace("{device}", device_name)
                        
            user_args = []
            if self.app_args:                
                app_args_str = self.app_args.replace('{window_title}', f'"{window_title}"')
                app_args_str = app_args_str.replace("{device}", device_name)
                user_args = shlex.split(app_args_str)
                        
            if self.app == "mpv":                
                if user_args:
                    args_list = user_args                    
                    has_title = any(arg.startswith('--title') for arg in args_list)
                    if not has_title:
                        args_list.append(f"--title={window_title}")
                else:                    
                    args_list = ["--force-window", f"--title={window_title}"]
            else:                
                args_list = user_args
                        
            if self.app == "mpv" and not any(arg == '--force-window' for arg in args_list):
                args_list.append("--force-window")
                        
            cmd = [self.app] + args_list + [url]

            if self.app == "mpv" and ("youtube.com" in url or "youtu.be" in url):
                cmd.append("--ytdl-format=best")
            
            if self.debug_mode:
                print(f"[DEBUG] Starting playback from {device_name}")
                print(f"[DEBUG] Command: {' '.join(cmd)}")
                print(f"[DEBUG] Window title: {window_title}")
                print(f"[DEBUG] User args: {self.app_args}")
                print(f"[DEBUG] Title arg: {self.title}")
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
            
            def monitor_output():
                for line in process.stdout:
                    if self.debug_mode and ('Playing:' in line or 'Video:' in line):
                        print(f"[DEBUG] ▶️  {line.strip()}")
            
            threading.Thread(target=monitor_output, daemon=True).start()
            print(f"▶️ Playing video from {device_name} on {self.app}\n")
            
        except FileNotFoundError:
            print(f"❌ ERROR: {self.app} is not installed")
            print(f"💡 Install with: sudo apt install {self.app} / brew install {self.app} / sudo pacman -S {self.app}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def log_message(self, format, *args):
        if self.debug_mode:
            print(f"[HTTP] {args[0]} {args[1]} {args[2]} from {self.client_address[0]}")

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def main():
    parser = argparse.ArgumentParser(description='Cast to MPV (Server)')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    parser.add_argument('--show-ip', action='store_true', help='Show all local IP addresses')
    parser.add_argument('--port', type=int, default=8080, help='Port to listen on')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--app', type=str, default='mpv', help='Application to use for video playback')
    parser.add_argument('--app_args', type=str, default='', help='Arguments passed to the playback app')
    parser.add_argument('--title', type=str, default='Cast from {device}', help='Window title (use {device} for device name) (only for mpv or compatible)')
    
    args = parser.parse_args()
    local_ip = get_local_ip()

    if args.show_ip:
        print("")
        subprocess.run('ip -o -4 addr show | awk \'{split($4,a,"/"); printf "\\033[1;36m%-12s\\033[0m %s\\n", $2, a[1]}\'', 
                       shell=True, executable='/bin/bash')
        sys.exit(0)
    
    print("─" * 50)
    print("🎬 Cast To MPV (Server)")
    print("─" * 50)
    print(f"📶 Local IP: {local_ip}")
    print(f"📡 Port: {args.port}")
    if args.title != 'Cast from {device}' or args.debug:
        print(f"🏷️ Title: {args.title}")
    if args.debug:
        print(f"🐛 Debug: ✅ Enabled")
    print("─" * 50)
    print("\nWaiting for connections... (Ctrl+C to exit)\n")
        
    def make_handler(debug, title, app, app_args):
        def handler(*args, **kwargs):
            return VideoHandler(*args, debug=debug, title=title,app=app, app_args=app_args, **kwargs)
        return handler
    
    try:
        handler_class = make_handler(args.debug, args.title, args.app, args.app_args)
        server = HTTPServer((args.host, args.port), handler_class)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        server.server_close()
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()