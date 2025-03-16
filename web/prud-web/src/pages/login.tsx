import { Button, TextField } from "@mui/material";

import { login } from "@/util/prud";
import { useRef } from "react";
import { useRouter } from "next/router";

const App = () => {
  const unameRef = useRef("");
  const pwRef = useRef("");
  const router = useRouter();

  const doLogin = () => {
    const uname = unameRef.current.value;
    const pw = pwRef.current.value;
    if (!uname || !pw) {
      return;
    }
    login(uname, pw, router);
  };
  return (
    <main>
      <form noValidate autoComplete="off">
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
        <Button type="button" onClick={doLogin}>
          Login
        </Button>
      </form>
    </main>
  );
};

export default App;
