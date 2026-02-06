# -*- coding: utf-8 -*-
from bcc import BPF
import os
import time
import subprocess
import scramble_effect

# --- 1. NUCLEAR RESET (Kills 'Busy' errors) ---
def hard_reset():
    print("[!] Breaking kernel locks...")
    subprocess.run("sudo fuser -k /sys/kernel/debug/tracing/trace_pipe >/dev/null 2>&1", shell=True)
    subprocess.run("echo 0 > /sys/kernel/debug/tracing/tracing_on", shell=True)
    subprocess.run("echo > /sys/kernel/debug/tracing/trace", shell=True)
    subprocess.run("echo 1 > /sys/kernel/debug/tracing/tracing_on", shell=True)
    time.sleep(0.5)

# --- 2. KERNEL LOGIC (The 'Unstuffer') ---
shaff_global_c = r"""
#include <uapi/linux/ptrace.h>

int kprobe__vfs_write(struct pt_regs *ctx) {
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    char comm[16];
    bpf_get_current_comm(&comm, sizeof(comm));

    char *buf = (char *)PT_REGS_PARM2(ctx);
    size_t count = PT_REGS_PARM3(ctx);

    if (count == 1) {
        char c;
        bpf_probe_read_kernel(&c, 1, buf);
        if (c == 0x2A) {
            bpf_trace_printk("MASK_DETECTED\n");
        }
    }
    return 0;
}
"""

if os.geteuid() != 0:
    print("Error: Must run as sudo!")
    exit()

hard_reset()

try:
    # Initialize BPF
    b = BPF(text=shaff_global_c)
    print("\033[1;32m[+] KERNEL HOOKED. SHAF ACTIVE.\033[0m")
   
    # Trigger the Premium Scramble Effect on Startup
    print("\033[1;31m[!] Unauthorized Kernel Write Detected!\033[0m")
    scramble_effect.run_scramble_effect(duration=3) 
    
    # --- 3. THE MAIN LOOP ---
    print("\033[1;36m[+] Monitoring for events...\033[0m")
    while True:
        # The Japanese Stuffon (Noise Layer)
        print("\033[1;35m[!] 信号ジャンボ_STUFFON_ACTIVE_0xDEADBEEF_紫のノイズ\033[0m")
        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("\n[!] Stealth Exit...")
