import "@/assets/tailwind.css";

import { ArrowLeftCircleIcon } from "@heroicons/react/24/outline";
import Link from "next/link";

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
  return (
    <div className="bg-slate-800/95 w-full flex flex-row h-24 items-center text-white sticky top-0 z-10">
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
    </div>
  );
};

export default TitleBar;
