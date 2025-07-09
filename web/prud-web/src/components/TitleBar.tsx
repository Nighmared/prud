import "@/assets/tailwind.css";

import { getLoginState, isAdmin, isAuthed, logout } from "@/util/prud";
import { useEffect, useState } from "react";

import { ArrowLeftCircleIcon } from "@heroicons/react/24/outline";
import { Button } from "@mui/material";
import Link from "next/link";
import { useRouter } from "next/router";

interface Props {
  title: string;
  backButton?: boolean;
  titleLink?: string;
}

const TitleBar: React.FC<Props> = ({
  title,
  backButton = false,
  titleLink = "/",
}) => {
  const [showLogout, setShowLogout] = useState(false);
  const router = useRouter();
  const doLogout = () => {
    logout();
    router.reload();
  };
  useEffect(() => {
    if (!router.isReady) return;
    setShowLogout(isAuthed());
  }, [router.isReady]);
  return (
    <div className="bg-slate-800/95 w-full flex flex-row h-24 items-center text-white sticky top-0 z-10 ">
      <div className="flex h-5/6 w-1/6 justify-center ">
        {backButton && (
          <Link href=".." className="flex w-full items-center justify-center">
            <ArrowLeftCircleIcon className="self-auto h-[60%] sm:h-[80%]" />
          </Link>
        )}
      </div>
      <div className="flex h-2/3 w-4/6  text-4xl sm:text-5xl md:text-6xl justify-center align-text-bottom  hover:underline">
        <a
          className="flex items-center"
          href={titleLink}
          target={titleLink == "/" ? "" : "_blank"}
        >
          {title}
        </a>
      </div>
      <div className="flex w-1/6 items-center justify-end pr-5   right-0">
        {showLogout && (
          <>
            <div className="pr-5 flex flex-col text-center">
              <span>{getLoginState()?.username}</span>
              <span>{getLoginState()?.email}</span>
              <span>Role: {getLoginState()?.role}</span>
            </div>
            <Button
              type="button"
              className="border-solid rounded-xl border-3 p-l-5 p-r-5 bg-white bg-opacity-100 hover:bg-gray-300"
              onClick={doLogout}
            >
              Logout
            </Button>
          </>
        )}
      </div>
    </div>
  );
};

export default TitleBar;
