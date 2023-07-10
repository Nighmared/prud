import { useEffect, useState } from "react";

export type Feed = {
    id: Number;
    title: string;
    url: string;
    feed: string;
    enabled: boolean;
}

export type ReadFeedsResponse = {
    feeds: Feed[];
}

export type Post = {
    title: string;
    link: string;
    summary: string;
    published: Number;
}

export type ReadPostsResponse = {
    feed: Feed;
    posts: Post[];
}



async function fetchApi<ResponseType>(url: string): Promise<ResponseType> {
    const response = fetch(url,);
    return (await response).json();
}

export async function readFeeds(setFeeds: Function) {
    const result = await fetchApi<ReadFeedsResponse>("/api/feeds");
    setFeeds(result.feeds)
}

export async function fetchReadPosts(feed_id: Number, setResult: Function) {
    const result = await fetchApi<ReadPostsResponse>(`/api/feeds/${feed_id}`)
    setResult(result);
}




