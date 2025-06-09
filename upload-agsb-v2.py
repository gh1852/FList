#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import streamlit as st
import sys

def run_external_script_with_vars(uuid, vmpt, agn, agk, script_url):
    # 构建要由 bash 执行的完整命令字符串
    # 注意：这里我们构造的是 bash 会执行的字符串，而不是直接给 shell=True 的字符串
    inner_command = (
        f"nix=y uuid={uuid} vmpt={vmpt} agn={agn} agk={agk} "
        f"bash <(curl -Ls {script_url})"
    )
    # 将整个命令字符串作为参数传递给 bash -c
    # 这样，无论 /bin/sh 指向什么，我们都确保是 bash 在处理命令
    command_to_execute = ["bash", "-c", inner_command]
    print(f"将要执行的命令 (通过 bash -c):\n{' '.join(command_to_execute)}\n")
    try:
        process = subprocess.run(
            command_to_execute, # 注意这里是列表，不再需要 shell=True
            check=True,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        print(f"\n命令成功执行，返回码: {process.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"\n命令执行失败，退出码: {e.returncode}", file=sys.stderr)
        print(f"标准输出:\n{e.stdout}", file=sys.stderr)
        print(f"标准错误:\n{e.stderr}", file=sys.stderr)
    except FileNotFoundError:
        print("错误: 找不到 bash 或 curl 命令。请确保它们已安装并添加到PATH环境变量中。", file=sys.stderr)
    except Exception as e:
        print(f"执行命令时发生意外错误: {e}", file=sys.stderr)

if __name__ == "__main__":
    # --- 配置你的变量 ---
    my_uuid = "7bbedb15-6e10-4727-bd0d-17db9d58a83d"
    my_vmpt = "8080"
    my_agn = st.secrets["agn"]  # 替换为你的实际域名
    my_agk = st.secrets["agk"]    # 替换为你的实际 token
    my_script_url = st.secrets["url"] # 替换为你的实际脚本 URL

    # --- 调用函数执行命令 ---
    run_external_script_with_vars(my_uuid, my_vmpt, my_agn, my_agk, my_script_url)
