import { useEffect, useState } from "react";

import Link from "next/link";
import { isAuthed } from "@/util/prud";
import { useRouter } from "next/router";

interface Props {}

const Footer: React.FC<Props> = (props) => {
  const [showLogin, setShowLogin] = useState(false);
  const router = useRouter();
  useEffect(() => {
    if (!router.isReady) return;
    setShowLogin(!isAuthed());
  });
  return (
    <>
      {showLogin && (
        <div className="fixed w-full bottom-0 right-0 pb-3 pr-2 text-right">
          <Link
            href="/login"
            className=" bg-slate-100 hover:bg-gray-300 p-2 border-solid rounded-xl"
          >
            Login
          </Link>
        </div>
      )}
    </>
  );
};

export default Footer;
