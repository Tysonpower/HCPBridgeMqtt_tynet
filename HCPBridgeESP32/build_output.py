Import('env')
import shutil
import os

def post_program_action(source, target, env):

    print("Moving firmware files to fw folder...")

    os.makedirs(os.path.dirname(os.path.join(env["PROJECT_DIR"], "fw")), exist_ok=True)
    fw_path = os.path.join(env["PROJECT_DIR"], "fw", env["PROGNAME"]+".bin")
    src = os.path.join(env["PROJECT_DIR"], ".pio", "build", env["PROGNAME"], env["PROGNAME"]+".bin")
    shutil.copy(src, fw_path)

    # merged file for webflash
    fw_path = os.path.join(env["PROJECT_DIR"], "fw", env["PROGNAME"]+"_merged.bin")
    src = os.path.join(env["PROJECT_DIR"], ".pio", "build", env["PROGNAME"], env["PROGNAME"]+"_merged.bin")
    shutil.copy(src, fw_path)

def merge_bin(source, target, env):
    build_dir = env.subst("$BUILD_DIR")
    app_elf = str(source[0])
    app_bin = app_elf.replace(".elf", ".bin")
    target_path = os.path.join(build_dir, env["PROGNAME"]+"_merged.bin")
    
    # tool paths
    platform = env.PioPlatform()
    esptool_path = os.path.join(platform.get_package_dir("tool-esptoolpy") or "", "esptool.py")
    python_path = env.subst("$PYTHONEXE")
    
    # find boot_app0.bin:
    framework_dir = platform.get_package_dir("framework-arduinoespressif32")
    boot_app0_path = os.path.join(framework_dir, "tools", "partitions", "boot_app0.bin")

    # create file list
    images = [
        ("0x0000", f'"{os.path.join(build_dir, "bootloader.bin")}"'),
        ("0x8000", f'"{os.path.join(build_dir, "partitions.bin")}"'),
        ("0xe000", f'"{boot_app0_path}"'),
        ("0x10000", f'"{app_bin}"')
    ]

    cmd = [
        f'"{python_path}"',
        f'"{esptool_path}"',
        '--chip esp32s3',
        'merge_bin',
        '-o', f'"{target_path}"',
        '--flash_mode dio',
        '--flash_freq 80m',
        '--flash_size 8MB'
    ]

    for addr, path in images:
        cmd.append(addr)
        cmd.append(path)

    print("\n--- STARTE MERGE PROCESS ---")
    full_cmd = " ".join(cmd)
    print(full_cmd)
    
    if os.system(full_cmd) == 0:
        print(f"--- OK! File: {target_path} ---\n")
    else:
        print("--- Error while merging firmware ---\n")

env.Replace(PROGNAME="%s" % env.subst("$PIOENV"))
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", merge_bin)
env.AddPostAction("$BUILD_DIR/${PROGNAME}.bin", post_program_action)