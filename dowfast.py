import os
import sys
import yt_dlp

BANNER = """
Oooooooooo.                                                .o88o.                        .
`888'   `Y8b                                               888 `"                      .o8
 888      888  .ooooo.  oooo oooo    ooo ooo. .oo.        o888oo   .oooo.    .oooo.o .o888oo
 888      888 d88' `88b  `88. `88.  .8'  `888P"Y88b        888    `P  )88b  d88(  "8   888
 888      888 888   888   `88..]88..8'    888   888        888     .oP"888  `"Y88b.    888
 888     d88' 888   888    `888'`888'     888   888        888    d8(  888  o.  )88b   888 .
o888bood8P'   `Y8bod8P'     `8'  `8'     o888o o888o      o888o   `Y888""8o 8""888P'   "888"
Logo-free video downloader for Linux | Multi-platform"""

def progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
        downloaded_bytes = d.get('downloaded_bytes', 0)
        
        if total_bytes > 0:
            percent = int(downloaded_bytes / total_bytes * 100)
            bar_length = 20
            filled_length = int(bar_length * percent // 100)
            bar = '=' * filled_length + ' ' * (bar_length - filled_length)
            
            mb_downloaded = downloaded_bytes / (1024 * 1024)
            
            sys.stdout.write(f"\rLoading [{bar}] {percent}% - {mb_downloaded:.1f}MB")
            sys.stdout.flush()
    elif d['status'] == 'finished':
        print("\n[+] Raw data stream has been loaded, post-processing is underway...")

def main():
    print(BANNER)
    
    url = input("[?] Your link: ").strip()
    if not url:
        print("[-] The link must not be empty.")
        return

    fmt_choice = input("[?] Which format do you want to download in? For example, enter [mp3/mp4]: ").strip().lower()
    
    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'quiet': True,
        'no_warnings': True
    }

    if fmt_choice == 'mp3':
        print("[*]Tools that support MP3 include")
        print(" - 64 - 96 kbps (HE-AAC v2 / MP3 short)")
        print(" - 128 - 160 kbps (Standard MP3/AAC)")
        print(" - 256 - 320 kbps (High Quality MP3/AAC)")
        print(" - 500 - 990 kbps (LDAC / aptX HD)")
        
        bitrate = input("[?]Enter preferred bitrate (e.g., 320): ").strip()
        
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': bitrate if bitrate else '320',
            }]
        })

    elif fmt_choice == 'mp4':
        print("[*]For mp4")
        print(" - 144p (256 x 144)")
        print(" - 240p (426 x 240)")
        print(" - 360p (640 x 360)")
        print(" - 480p (854 x 480)")
        print(" - 720p (1280 x 720)")
        print(" - 1080p (1920 x 1080)")
        print(" - 1440p (2560 x 1440)")
        print(" - 2160p (3840 x 2160)")
        print(" - 4320p (7680 x 4320)")
        
        res = input("[?] Enter resolution height (e.g., 1080): ").strip()
        fps = input("[?] Almost finished. How many FPS do you want to load at? For example, enter [30/60]: ").strip()
        
        print("[!] Warning: Higher quality means larger storage capacity, so please ensure your device is powerful enough")
        
        res_val = res if res else '1080'
        fps_val = fps if fps else '60'
        ydl_opts.update({
            'format': f'bestvideo[height<={res_val}][fps<={fps_val}]+bestaudio/best',
            'merge_output_format': 'mp4'
        })
    else:
        print("[-] Format not supported. Please select mp3 or mp4")
        return

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("[+] Completed, please check")
    except Exception as e:
        print(f"\n[-] An error occurred: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] You have just canceled the process")

