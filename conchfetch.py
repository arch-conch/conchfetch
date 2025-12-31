#!/usr/bin/env python3
import subprocess
import os
import platform
from typing import Dict

version = 1.0

logos = {
        'arch': """
         █████╗ ██████╗  ██████╗██╗  ██╗
        ██╔══██╗██╔══██╗██╔════╝██║  ██║
        ███████║██████╔╝██║     ███████║
        ██╔══██║██╔══██╗██║     ██╔══██║
        ██║  ██║██║  ██║╚██████╗██║  ██║
        ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
        """,
        'debian': """
        ██████╗ ███████╗██████╗ ██╗ █████╗ ███╗   ██╗
        ██╔══██╗██╔════╝██╔══██╗██║██╔══██╗████╗  ██║
        ██║  ██║█████╗  ██████╔╝██║███████║██╔██╗ ██║
        ██║  ██║██╔══╝  ██╔══██╗██║██╔══██║██║╚██╗██║
        ██████╔╝███████╗██████ ║██║██║  ██║██║ ╚████║
        ╚═════╝ ╚══════╝╚══════╝╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
        """,
        'ubuntu': """
        ██╗   ██╗██████╗ ██╗   ██╗███╗   ██╗████████╗██╗   ██╗
        ██║   ██║██╔══██╗██║   ██║████╗  ██║╚══██╔══╝██║   ██║
        ██║   ██║██████╔╝██║   ██║██╔██╗ ██║   ██║   ██║   ██║
        ██║   ██║██╔══██╗██║   ██║██║╚██╗██║   ██║   ██║   ██║
        ╚██████╔╝██████╔╝╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝
         ╚═════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝
        """,
        'default': """
        ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
        ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
        ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝ 
        ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗ 
        ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
        ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
        """
    }

def get_distro_name() -> str:
    # Get distribution name
    try:
        with open('/etc/os-release', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'PRETTY_NAME' in line:
                    return line.split('=')[1].strip().strip('"')
    except:
        pass

    # Alternative methods
    for file in ['/etc/lsb-release', '/etc/redhat-release', '/etc/debian_version']:
        try:
            with open(file, 'r') as f:
                return f.readline().strip()
        except:
            continue

    return "Unknown Linux"


def get_kernel_version() -> str:
    # Get kernel version
    return platform.release()


def get_uptime() -> str:
    # Get system uptime
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])

        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)

        if hours >= 24:
            days = hours // 24
            hours = hours % 24
            return f"{days}d {hours}h {minutes}m"
        else:
            return f"{hours}h {minutes}m"
    except:
        return "Unknown"


def get_shell() -> str:
    # Get current shell
    shell = os.environ.get('SHELL', 'Unknown')
    return os.path.basename(shell)


def get_terminal() -> str:
    # Get current terminal
    term = os.environ.get('TERM', 'Unknown')
    term_program = os.environ.get('TERM_PROGRAM', '')

    if term_program:
        return term_program
    return term


def get_packages_count() -> str:
    # Get count of installed packages
    try:
        # For different package managers
        for manager, cmd in [
            ('dpkg', ['dpkg', '--list']),
            ('rpm', ['rpm', '-qa']),
            ('pacman', ['pacman', '-Q']),
            ('xbps', ['xbps-query', '-l']),
            ('apk', ['apk', 'info'])
        ]:
            try:
                if manager == 'dpkg':
                    result = subprocess.run(['dpkg', '--list'], capture_output=True, text=True)
                    if result.returncode == 0:
                        count = len([line for line in result.stdout.split('\n') if line.startswith('ii')])
                        return f"{count} (dpkg)"
                elif manager == 'pacman':
                    result = subprocess.run(['pacman', '-Q'], capture_output=True, text=True)
                    if result.returncode == 0:
                        count = len(result.stdout.strip().split('\n'))
                        return f"{count} (pacman)"
                else:
                    result = subprocess.run(cmd[0], capture_output=True, text=True)
                    if result.returncode == 0:
                        count = len(result.stdout.strip().split('\n'))
                        return f"{count} ({manager})"
            except:
                continue
    except:
        pass
    return "Unknown"


def get_cpu_info() -> str:
    # Get CPU information
    try:
        with open('/proc/cpuinfo', 'r') as f:
            lines = f.readlines()
            for line in lines:
                if 'model name' in line.lower():
                    cpu = line.split(':', 1)[1].strip()
                    # Remove extra information
                    cpu = cpu.replace('(R)', '').replace('(TM)', '').replace('CPU', '')
                    return cpu.split('@')[0].strip() if '@' in cpu else cpu
    except:
        pass
    return "Unknown CPU"


def get_memory_info() -> Dict[str, float]:
    # Get memory information in MB
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
            meminfo = {}
            for line in lines:
                if 'MemTotal' in line or 'MemAvailable' in line or 'SwapTotal' in line:
                    key, value = line.split(':')
                    meminfo[key.strip()] = int(value.strip().replace(' kB', '')) / 1024

            return {
                'total': meminfo.get('MemTotal', 0),
                'available': meminfo.get('MemAvailable', 0),
                'swap': meminfo.get('SwapTotal', 0)
            }
    except:
        return {'total': 0, 'available': 0, 'swap': 0}


def get_disk_usage() -> str:
    # Get disk usage information
    try:
        result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) > 1:
                parts = lines[1].split()
                if len(parts) >= 5:
                    return f"{parts[4]} used ({parts[2]}/{parts[1]})"
    except:
        pass
    return "Unknown"


def get_gpu_info() -> str:
    # Get GPU information - minimal version
    # First try nvidia-smi
    try:
        result = subprocess.run(
            ['nvidia-smi', '--query-gpu=name', '--format=csv,noheader'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                return output  # Return as is
    except:
        pass

    # If nvidia-smi failed, try lspci
    try:
        result = subprocess.run(
            ['bash', '-c', 'lspci | grep -i "VGA\\|3D" | head -1 | cut -d: -f3 | sed "s/^ //"'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if output:
                return output
    except:
        pass

    return "Unknown GPU"


def get_hostname() -> str:
    # Get hostname
    return platform.node()


def print_logo():
    # Print ASCII logo


    distro = get_distro_name().lower()
    if 'arch' in distro:
        print(logos['arch'])
    elif 'debian' in distro:
        print(logos['debian'])
    elif 'ubuntu' in distro:
        print(logos['ubuntu'])
    else:
        print(logos['default'])


def get_resolution() -> str:
    # Get screen resolution
    try:
        # Try simple xrandr with filtering
        result = subprocess.run(
            "xrandr 2>/dev/null | grep -w connected | grep -oP '[0-9]+x[0-9]+' || true",
            shell=True,
            capture_output=True,
            text=True,
            timeout=3
        )

        if result.returncode == 0:
            resolutions = result.stdout.strip().split()
            if resolutions:
                # Filter incorrect values
                valid_resolutions = []
                for res in resolutions:
                    if 'x' in res:
                        try:
                            w, h = map(int, res.split('x'))
                            if 100 <= w <= 10000 and 100 <= h <= 10000:
                                valid_resolutions.append(res)
                        except:
                            continue

                if valid_resolutions:
                    # If multiple monitors with same resolution
                    unique_res = list(set(valid_resolutions))
                    if len(unique_res) == 1:
                        return unique_res[0]
                    else:
                        return f"{len(unique_res)} displays: {', '.join(unique_res)}"

    except:
        pass

    # Try through xdpyinfo as fallback
    try:
        result = subprocess.run(
            "xdpyinfo 2>/dev/null | grep dimensions | awk '{print $2}'",
            shell=True,
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0 and result.stdout.strip():
            res = result.stdout.strip()
            if 'x' in res:
                return res
    except:
        pass

    return "Not detected"


def print_info():
    # Main function to print information
    print_logo()

    # Colors (can be changed)
    color_start = "\033[1;36m"  # Cyan
    color_end = "\033[0m"

    distro = get_distro_name()
    kernel = get_kernel_version()
    host = get_hostname()
    uptime = get_uptime()
    packages = get_packages_count()
    shell = get_shell()
    terminal = get_terminal()
    cpu = get_cpu_info()
    memory = get_memory_info()
    disk = get_disk_usage()
    gpu = get_gpu_info()
    resolution = get_resolution()

    used_memory = memory['total'] - memory['available']
    memory_percent = (used_memory / memory['total']) * 100 if memory['total'] > 0 else 0

    info_lines = [
        f"{color_start}┌──────────────────────────────────────────────┐{color_end}",
        f"{color_start}  OS:{color_end} {distro:50}",
        f"{color_start}  Packages:{color_end} {packages:44}",
        f"{color_start}  Host:{color_end} {host:49}",
        f"{color_start}  Kernel:{color_end} {kernel:47}",
        f"{color_start}  Uptime:{color_end} {uptime:47}",
        f"{color_start}  Shell:{color_end} {shell:48}",
        f"{color_start}  Terminal:{color_end} {terminal:45}",
        f"{color_start}  Resolution:{color_end} {resolution:42}",
        f"",
        f"{color_start}  GPU:{color_end} {gpu}",
        f"{color_start}  CPU:{color_end} {cpu[:50]:50}",
        f"{color_start}  Mem:{color_end} {used_memory:.1f}MB / {memory['total']:.1f}MB ({memory_percent:.1f}%)",
        f"",
        f"{color_start}  Swap:{color_end} {memory['swap']:.1f}MB{'' if memory['swap'] == 0 else ' available':42}",
        f"{color_start}  Disk:{color_end} {disk:47}",
        f"",
        f"{color_start}  conchfetch version: {color_end}{version}",
        f"{color_start}└───────────────────────────────────────────────┘{color_end}"
    ]

    for line in info_lines:
        print(line)


if __name__ == "__main__":
    print_info()
    quit()