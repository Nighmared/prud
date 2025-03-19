import { Button, TextField } from "@mui/material";
import { FormEvent, useRef } from "react";

import { login } from "@/util/prud";
import { useRouter } from "next/router";

const App = () => {
  const unameRef = useRef("");
  const pwRef = useRef("");
  const router = useRouter();

  const doLogin = (event: FormEvent) => {
    event.preventDefault();
    const uname = unameRef.current.value;
    const pw = pwRef.current.value;
    if (!uname || !pw) {
      // console.log(unameRef);
      return;
    }
    login(uname, pw, router);
  };
  return (
    <main>
      <div className="flex-col h-screen align-middle justify-center border-2 border-red-600 border-solid place-content-center justify-items-center">
        <div className="flex-row w-full justify-center text-center">
          <div>
            <form autoComplete="off" onSubmit={doLogin}>
              <TextField
                type="text"
                required
                label="Username"
                name="username"
                inputRef={unameRef}
              ></TextField>
              <TextField
                type="password"
                required
                label="Password"
                name="password"
                inputRef={pwRef}
              ></TextField>
              <Button type="submit">Login</Button>
            </form>
          </div>
        </div>
      </div>
    </main>
  );
};

export default App;
