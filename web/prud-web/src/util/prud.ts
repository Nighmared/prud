export type Feed = {
  id: Number;
  title: string;
  url: string;
  feed: string;
  enabled: boolean;
  disabled_until?: number;
};

export type ReadFeedsResponse = {
  feeds: Feed[];
};

export type Post = {
  title: string;
  link: string;
  summary: string;
  published: number;
};

export type ReadPostsResponse = {
  feed: Feed;
  posts: Post[];
};

async function fetchApi<ResponseType>(url: string): Promise<ResponseType> {
  const response = fetch(url);
  return (await response).json();
}

export async function readFeeds(setFeeds: Function) {
  //XXX hack for debugging...
  if (document.location.host.includes("localhost")) {
    const result = await fetchApi<ReadFeedsResponse>(
      "http://localhost:8801/api/feeds"
    );
    setFeeds(result.feeds);
    return;
  } else {
    const result = await fetchApi<ReadFeedsResponse>("/api/feeds");
    setFeeds(result.feeds);
  }
}

export async function fetchReadPosts(feed_id: Number, setResult: Function) {
  //XXX hack for debugging...
  if (document.location.host.includes("localhost")) {
    const result = await fetchApi<ReadPostsResponse>(
      `http://localhost:8801/api/feeds/${feed_id}`
    );
    setResult(result);
  } else {
    const result = await fetchApi<ReadPostsResponse>(`/api/feeds/${feed_id}`);
    setResult(result);
  }
}
