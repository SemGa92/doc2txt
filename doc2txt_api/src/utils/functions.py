import base64
import subprocess as sp


def decode_bs64_to_file(f_out: str, bs64: str) -> None:
    """It decodes base64 input string to document extension"""
    with open(f_out, 'wb') as f:
        f.write(base64.b64decode(bs64))


def subprocess_mgr(cmd: list[str], sp_type: str, time_out: int) -> None:
    """Open a subprocess and wait till its end"""
    try:
        proc = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE)
        _, _ = proc.communicate(timeout=time_out)
    except sp.TimeoutExpired:
        proc.terminate()
        raise sp.TimeoutExpired(sp_type, time_out)
