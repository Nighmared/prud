import { Button, TextField } from "@mui/material";
import { FormEvent, useRef } from "react";

import { login } from "@/util/prud";
import { useRouter } from "next/router";

const App = () => {
  const router = useRouter();

  const doLogin = (event: FormEvent) => {
    event.preventDefault();
    const unameval = (document.getElementById("uname") as HTMLInputElement)
      .value;
    const pwval = (document.getElementById("pw") as HTMLInputElement).value;
    if (!unameval || !pwval) {
      return;
    }
    login(unameval, pwval, router);
  };
  return (
    <main>
      <div className="flex-col h-screen align-middle justify-center border-2 border-red-600 border-solid place-content-center justify-items-center">
        <div className="flex-row w-full justify-center text-center">
          <div>
            <form autoComplete="off" onSubmit={doLogin}>
              <TextField
                id="uname"
                type="text"
                required
                label="Username"
                name="username"
              ></TextField>
              <TextField
                id="pw"
                type="password"
                required
                label="Password"
                name="password"
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
