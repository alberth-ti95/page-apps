from subprocess import run, CalledProcessError
from tkinter import messagebox, simpledialog
import os


def _run_git_cmd(args):
    return run(
        ["git"] + args,
        check=True,
        capture_output=True,
        text=True,
    )


def update():
    comentario = simpledialog.askstring(
        "GitHub", "Escolheu 'UPDATE'\nComentário/versão\t\t"
    )

    if not comentario or not comentario.strip():
        messagebox.showwarning("GitHub", "Comentário em branco")
        return

    try:
        _run_git_cmd(["add", "."])
        _run_git_cmd(["commit", "-m", comentario])
        _run_git_cmd(["push"])

        messagebox.showinfo("GitHub", "Update realizado com sucesso!")

    except CalledProcessError as e:
        messagebox.showerror("GitHub", f"Erro ao executar o git.\n\n{e.stderr}")


def primeiro_commit():
    comentario = simpledialog.askstring(
        "GitHub", "Escolheu 'PRIMEIRO COMMIT'\nComentário/versão\t\t"
    )

    if not comentario or not comentario.strip():
        messagebox.showwarning("GitHub", "Comentário em branco")
        return

    comentario = comentario.replace("'", "").replace('"', "")

    try:
        url_repo = simpledialog.askstring("GitHub", "URL do repositório")
        if not url_repo or not url_repo.strip():
            messagebox.showwarning("GitHub", "URL do repositório não informada")
            return

        _run_git_cmd(["init"])
        _run_git_cmd(["branch", "-M", "main"])
        _run_git_cmd(["add", "."])
        _run_git_cmd(["commit", "-m", f"Primeiro commit {comentario}"])
        _run_git_cmd(["remote", "add", "origin", url_repo])
        _run_git_cmd(["push", "-u", "origin", "main"])

        messagebox.showinfo("GitHub", "Primeiro commit realizado com sucesso!")

    except CalledProcessError as e:
        messagebox.showerror("GitHub", f"Erro ao executar o git.\n\n{e.stderr}")


def iniciar():
    from threading import Thread

    caminho = os.path.dirname(os.path.abspath(__file__))
    os.chdir(caminho)

    print(f"\n\nONDE ESTOU? {caminho}\n\n")

    menu = {
        1: update,
        2: primeiro_commit,
    }

    opcao = "\n".join(f"{a} - {b.__name__}" for a, b in menu.items())

    executar = simpledialog.askinteger(
        "GitHub", f"Local:\t{caminho}\n\nQual opção:\n{opcao}"
    )

    if executar in menu:
        Thread(target=menu[executar]).start()
    elif executar is not None:
        messagebox.showwarning("GitHub", "Opção inválida")


if __name__ == "__main__":
    iniciar()
