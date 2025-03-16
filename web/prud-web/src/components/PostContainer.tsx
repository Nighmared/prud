import { Divider, Typography } from "@mui/material";
import { Post, deletePost } from "@/util/prud";

import { useRouter } from "next/router";

interface Props {
  post: Post;
  userIsAdmin: boolean;
  reloadPostsCallback: () => void;
}

const PostContainer: React.FC<Props> = ({
  post,
  userIsAdmin,
  reloadPostsCallback,
}) => {
  const published_txt = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(post.published * 1000);

  const doDelete = (postId: number) => {
    deletePost(postId);
    reloadPostsCallback();
  };

  const linkWithHttpEnsured = post.link.startsWith("http")
    ? post.link
    : `https://${post.link}`;
  return (
    <>
      <div>
        <div className="flex flex-row gap-2">
          <div className="flex w-full">
            <a
              className="hover:underline"
              href={linkWithHttpEnsured}
              target="_blank"
              rel="noreferrer noopener"
            >
              <Typography variant="h4">{post.title}</Typography>
              <Typography variant="subtitle1">{published_txt}</Typography>
              <Typography variant="body1" className="break-all">
                {post.summary.substring(0, 1000)}
              </Typography>
            </a>
          </div>
          <div className="flex w-min right-0">
            <button onClick={() => doDelete(post.id)}>
              {userIsAdmin ? "❌" : ""}
            </button>
          </div>
        </div>
      </div>
      <Divider />
    </>
  );
};

export default PostContainer;
