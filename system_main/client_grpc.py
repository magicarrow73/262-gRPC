import tkinter as tk
import threading
import grpc
import argparse
import os

import chat_pb2
import chat_pb2_grpc

from utils import hash_password

CLIENT_LOG_FILE = "client_data_usage.log"

def log_data_usage(method_name: str, request_size: int, response_size: int):
    """
    Append data usage (req_size, resp_size) to a local file with a header if needed.
    """
    file_exists = os.path.exists(CLIENT_LOG_FILE)
    if not file_exists:
        with open(CLIENT_LOG_FILE, "w") as f:
            f.write("method_name,request_size,response_size\n")

    with open(CLIENT_LOG_FILE, "a") as f:
        f.write(f"{method_name},{request_size},{response_size}\n")

class TkClientGRPC:
    def __init__(self, host="127.0.0.1", port=12345):
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None

        self.current_user = None
        self.subscribe_thread = None
        self.subscribe_stop_event = threading.Event()

        # GUI Setup
        self.root = tk.Tk()
        self.root.title("gRPC Chat Client")

        self.text_area = tk.Text(self.root, state='disabled', width=80, height=20)
        self.text_area.pack()

        self.entry = tk.Entry(self.root, width=80)
        self.entry.pack()

        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack()

        tk.Button(self.btn_frame, text="Create Account", command=self.create_account_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Login", command=self.login_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Logout", command=self.logout_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Send", command=self.send_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="List", command=self.list_accounts_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Read", command=self.read_messages_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Delete Msg", command=self.delete_msg_dialog).pack(side=tk.LEFT)
        tk.Button(self.btn_frame, text="Delete Account", command=self.delete_account).pack(side=tk.LEFT)

    def connect(self):
        address = f"{self.host}:{self.port}"
        self.channel = grpc.insecure_channel(address)
        self.stub = chat_pb2_grpc.ChatServiceStub(self.channel)
        self.log(f"Connected to gRPC server at {address}")

    def log(self, msg):
        """
        Logs to the GUI text area.
        """
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.config(state='disabled')
        self.text_area.see(tk.END)

    # ------------- Subscription / Push Handling ------------- #

    def start_subscription_thread(self):
        if not self.current_user:
            return
        self.subscribe_stop_event.clear()

        def run_stream():
            request = chat_pb2.SubscribeRequest(username=self.current_user)
            try:
                for incoming in self.stub.Subscribe(request):
                    if self.subscribe_stop_event.is_set():
                        break
                    sender = incoming.sender
                    content = incoming.content
                    self.log(f"[New Message] from={sender}: {content}")
            except grpc.RpcError as e:
                self.log(f"[Subscription ended] {e.details()}")

        self.subscribe_thread = threading.Thread(target=run_stream, daemon=True)
        self.subscribe_thread.start()

    def stop_subscription_thread(self):
        self.subscribe_stop_event.set()

    # ------------- Dialog & Command Implementations ------------- #

    def create_account_dialog(self):
        w = tk.Toplevel(self.root)
        w.title("Create Account")

        tk.Label(w, text="Username").pack()
        user_entry = tk.Entry(w)
        user_entry.pack()

        tk.Label(w, text="Password").pack()
        pass_entry = tk.Entry(w, show="*")
        pass_entry.pack()

        tk.Label(w, text="Display Name").pack()
        disp_entry = tk.Entry(w)
        disp_entry.pack()

        def on_ok():
            username = user_entry.get().strip()
            password = pass_entry.get()
            display = disp_entry.get()
            w.destroy()

            hashed_pw = hash_password(password)
            req = chat_pb2.CreateUserRequest(
                username=username,
                hashed_password=hashed_pw,
                display_name=display
            )
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.CreateUser(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("CreateUser", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}")
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def login_dialog(self):
        w = tk.Toplevel(self.root)
        w.title("Login")

        tk.Label(w, text="Username").pack()
        user_entry = tk.Entry(w)
        user_entry.pack()

        tk.Label(w, text="Password").pack()
        pass_entry = tk.Entry(w, show="*")
        pass_entry.pack()

        def on_ok():
            username = user_entry.get().strip()
            password = pass_entry.get()
            w.destroy()

            hashed_pw = hash_password(password)
            req = chat_pb2.LoginRequest(username=username, hashed_password=hashed_pw)
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.Login(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("Login", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message} (unread={resp.unread_count})")
                if resp.status == "success":
                    self.current_user = resp.username
                    self.start_subscription_thread()
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def logout_dialog(self):
        if not self.current_user:
            self.log("[ERROR] No user is currently logged in.")
            return

        w = tk.Toplevel(self.root)
        w.title("Logout")
        tk.Label(w, text=f"Are you sure you want to logout {self.current_user}?").pack()

        def on_ok():
            w.destroy()
            self.stop_subscription_thread()

            req = chat_pb2.LogoutRequest(username=self.current_user)
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.Logout(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("Logout", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}")
                if resp.status == "success":
                    self.current_user = None
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def send_dialog(self):
        if not self.current_user:
            self.log("[ERROR] You are not logged in.")
            return

        w = tk.Toplevel(self.root)
        w.title("Send Message")

        tk.Label(w, text="To User").pack()
        to_entry = tk.Entry(w)
        to_entry.pack()

        tk.Label(w, text="Message").pack()
        msg_entry = tk.Entry(w)
        msg_entry.pack()

        def on_ok():
            receiver = to_entry.get().strip()
            content = msg_entry.get()
            w.destroy()

            req = chat_pb2.SendMessageRequest(
                sender=self.current_user,
                receiver=receiver,
                content=content
            )
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.SendMessage(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("SendMessage", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}")
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def list_accounts_dialog(self):
        if not self.current_user:
            self.log("[ERROR] You are not logged in.")
            return

        w = tk.Toplevel(self.root)
        w.title("List Accounts")

        tk.Label(w, text="Pattern (leave blank for all)").pack()
        pattern_entry = tk.Entry(w)
        pattern_entry.pack()

        list_frame = tk.Frame(w)
        list_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        account_listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, width=50, height=10)
        scrollbar.config(command=account_listbox.yview)
        account_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        def on_ok():
            pat = pattern_entry.get().strip() or "*"
            req = chat_pb2.ListUsersRequest(username=self.current_user, pattern=pat)
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.ListUsers(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("ListUsers", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}")
                account_listbox.delete(0, tk.END)
                for u in resp.users:
                    line = f"{u.username} ({u.display_name})"
                    self.log("  " + line)
                    account_listbox.insert(tk.END, line)
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def read_messages_dialog(self):
        if not self.current_user:
            self.log("[ERROR] You are not logged in.")
            return

        w = tk.Toplevel(self.root)
        w.title("Read Messages")

        unread_var = tk.BooleanVar(value=False)
        chk = tk.Checkbutton(w, text="Only Unread?", variable=unread_var)
        chk.pack()

        tk.Label(w, text="How many messages (blank for all)").pack()
        limit_entry = tk.Entry(w)
        limit_entry.pack()

        def on_ok():
            only_unread = unread_var.get()
            limit_str = limit_entry.get().strip()
            w.destroy()

            limit_val = 0
            if limit_str:
                try:
                    limit_val = int(limit_str)
                except ValueError:
                    self.log("[ERROR] Invalid integer for limit.")
                    return

            req = chat_pb2.ReadMessagesRequest(
                username=self.current_user,
                only_unread=only_unread,
                limit=limit_val
            )
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.ReadMessages(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("ReadMessages", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}")
                for m in resp.messages:
                    self.log(f"  ID={m.id}, from={m.sender_username}, content={m.content}")
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def delete_msg_dialog(self):
        if not self.current_user:
            self.log("[ERROR] You are not logged in.")
            return

        w = tk.Toplevel(self.root)
        w.title("Delete Message(s)")

        tk.Label(w, text="Message ID(s), comma separated").pack()
        msg_id_entry = tk.Entry(w)
        msg_id_entry.pack()

        def on_ok():
            raw_input = msg_id_entry.get().strip()
            w.destroy()
            if not raw_input:
                return

            parts = [p.strip() for p in raw_input.split(",") if p.strip()]
            msg_ids = []
            for p in parts:
                try:
                    msg_ids.append(int(p))
                except ValueError:
                    self.log("[ERROR] IDs must be numeric.")
                    return

            req = chat_pb2.DeleteMessagesRequest(
                username=self.current_user,
                message_ids=msg_ids
            )
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.DeleteMessages(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("DeleteMessages", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}, count={resp.deleted_count}")
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def delete_account(self):
        if not self.current_user:
            self.log("[ERROR] You are not logged in.")
            return

        w = tk.Toplevel(self.root)
        w.title("Delete Account")
        tk.Label(w, text=f"Are you sure you want to delete your account '{self.current_user}'?").pack()

        def on_ok():
            w.destroy()
            self.stop_subscription_thread()

            req = chat_pb2.DeleteUserRequest(username=self.current_user)
            req_size = len(req.SerializeToString())
            try:
                resp = self.stub.DeleteUser(req)
                resp_size = len(resp.SerializeToString())
                log_data_usage("DeleteUser", req_size, resp_size)

                self.log(f"[{resp.status.upper()}] {resp.message}")
                if resp.status == "success":
                    self.current_user = None
            except grpc.RpcError as e:
                self.log(f"[ERROR] {e.details()}")

        tk.Button(w, text="OK", command=on_ok).pack()

    def run(self):
        self.connect()
        self.root.mainloop()
        self.stop_subscription_thread()

def main():
    parser = argparse.ArgumentParser(description="gRPC Chat Client")
    parser.add_argument("--host", default="127.0.0.1",
                        help="Server host to connect to.")
    parser.add_argument("--port", type=int, default=12345,
                        help="Server port to connect to.")
    args = parser.parse_args()

    gui = TkClientGRPC(host=args.host, port=args.port)
    gui.run()

if __name__ == "__main__":
    main()
