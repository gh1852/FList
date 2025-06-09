#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import streamlit as st
import sys

def run_external_script_with_vars(uuid, vmpt, agn, agk, script_url):
    """
    使用指定的变量运行外部 Shell 脚本。

    Args:
        uuid (str): UUID 值。
        vmpt (str): VMPT 值。
        agn (str): AGN 值。
        agk (str): AGK 值。
        script_url (str): 外部 Shell 脚本的 URL。
    """
    # 构建完整的 shell 命令字符串
    # 注意：这里直接拼接字符串，变量值会被 shell 解释，确保它们不包含恶意字符。
    # 对于固定的值，通常风险较低。
    command = (
        f"nix=y uuid={uuid} vmpt={vmpt} agn={agn} agk={agk} "
        f"bash <(curl -Ls {script_url})"
    )

    print(f"将要执行的命令:\n{command}\n")

    try:
        # 使用 subprocess.run 执行命令
        # shell=True 是必须的，因为命令中包含了管道和进程替换 (<())
        # check=True 会在命令返回非零退出码时抛出 CalledProcessError
        # capture_output=False 意味着子进程的输出会直接打印到当前 Python 进程的控制台
        # 如果你想捕获输出到变量，请将 capture_output=True 并处理 result.stdout/stderr
        process = subprocess.run(
            command,
            shell=True,
            check=True,
            stdout=sys.stdout, # 将子进程的标准输出重定向到当前 Python 脚本的标准输出
            stderr=sys.stderr, # 将子进程的标准错误重定向到当前 Python 脚本的标准错误
            text=True # 确保输出是文本而非字节
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
