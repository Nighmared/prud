import { Post } from "@/util/prud";
import Link from "next/link";

interface Props {
    post: Post;
}

const PostContainer: React.FC<Props> = ({ post }) => {

    return (
        <>
            <div>
                <a href={post.link}>
                    {post.title}
                </a>
            </div>
        </>
    )
}


export default PostContainer