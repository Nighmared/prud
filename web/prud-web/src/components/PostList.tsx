import { List } from "@mui/material";
import { Post } from "@/util/prud";
import PostContainer from "./PostContainer";

interface Props {
  posts: Post[];
  userIsAdmin: boolean;
  reloadPostsCallback: () => void;
}

const PostList: React.FC<Props> = ({
  posts,
  userIsAdmin,
  reloadPostsCallback,
}) => {
  return (
    <>
      <List>
        {posts.map((p, i) => (
          <li key={i}>
            <PostContainer
              post={p}
              userIsAdmin={userIsAdmin}
              reloadPostsCallback={reloadPostsCallback}
            />
          </li>
        ))}
      </List>
    </>
  );
};

export default PostList;
