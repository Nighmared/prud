import { NextRouter } from "next/router";
import { jwtDecode } from "jwt-decode";

type TokenValues = {
  username: string;
  email: string;
  role: "ADMIN" | "DEFAULT";
  expires: Date;
};

export type LoginState = TokenValues & {
  token: string;
};

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
  id: number;
  title: string;
  link: string;
  summary: string;
  published: number;
};

export type ReadPostsResponse = {
  feed: Feed;
  posts: Post[];
};

type LoginResponse = {
  access_token: string;
  token_type: "bearer";
  expiry: number;
  error?: string;
};

type LoginRequest = {
  username: string;
  password: string;
  grant_type: string;
};

type DeletePostResponse = {
  info: string;
};

export type Session = {
  id: string;
};

export function getLoginURL(): URL {
  if (document.location.host.includes("localhost")) {
    return new URL("http://localhost:8801/api/login");
  }
  return new URL("/api/login");
}

async function fetchApiBodyMethod<ResponseType>(
  url: string,
  method: "POST" | "GET" | "DELETE" | "PATCH",
  headers: Headers,
  body?: string
): Promise<Response> {
  const rqInit: RequestInit = { method: method, headers: headers };
  if (!!body) {
    rqInit.body = body;
  }
  const response = fetch(url, rqInit);
  return await response;
}
async function fetchApiBodyMethodParse<ResponseType>(
  url: string,
  method: "POST" | "GET" | "DELETE" | "PATCH",
  headers: Headers,
  body?: string
): Promise<ResponseType> {
  return (await fetchApiBodyMethod(url, method, headers, body)).json();
}

async function fetchApi<ResponseType>(url: string): Promise<ResponseType> {
  const headers: Headers = new Headers();
  return fetchApiBodyMethodParse<ResponseType>(url, "GET", headers);
}

async function postApi<ResponseType>(
  url: string,
  body: string,
  headers: Headers = new Headers()
): Promise<ResponseType> {
  return fetchApiBodyMethodParse<ResponseType>(url, "POST", headers, body);
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

export async function login(
  username: string,
  password: string,
  router: NextRouter
) {
  const loginURL = getLoginURL();
  const data: LoginRequest = {
    username: username,
    password: password,
    grant_type: "password",
  };
  const params: URLSearchParams = new URLSearchParams(data);
  const headers = new Headers({
    "Content-Type": "application/x-www-form-urlencoded",
  });

  const result = await postApi<LoginResponse>(
    loginURL.toString(),
    params.toString(),
    headers
  );

  if (!!result.error) {
    console.log("bad login");
    return;
  }

  const decoded = jwtDecode<TokenValues>(result.access_token);

  document.cookie =
    "token=" + result.access_token + "; expires=" + result.expiry;
  window.sessionStorage.setItem("token", result.access_token);
  router.push("/");
}

export function logout() {
  document.cookie = "token=--";
  window.sessionStorage.removeItem("token");
}

export async function deletePost(postId: number) {
  const baseUrl = document.location.host.includes("localhost")
    ? "http://localhost:8801/api/posts/"
    : "/api/posts/";

  const headers = new Headers({
    Authorization: "Bearer " + getLoginState()?.token,
  });

  await fetchApiBodyMethod(baseUrl + postId, "DELETE", headers);
}

export async function deleteFeed(
  feedId: number,
  refreshFeedsCallback: () => void
) {
  const baseUrl = document.location.host.includes("localhost")
    ? "http://localhost:8801/api/feeds/"
    : "/api/feeds/";

  const headers = new Headers({
    Authorization: "Bearer " + getLoginState()?.token,
  });

  await fetchApiBodyMethod(
    baseUrl + feedId,
    "DELETE",
    headers,
    JSON.stringify({})
  );
  refreshFeedsCallback();
}

export async function enableFeed(feedId: number) {
  const baseUrl = document.location.host.includes("localhost")
    ? "http://localhost:8801/api/feeds/"
    : "/api/feeds/";

  const headers = new Headers({
    "Content-Type": "application/json",
    Authorization: "Bearer " + getLoginState()?.token,
  });

  await fetchApiBodyMethod(
    baseUrl + feedId,
    "PATCH",
    headers,
    JSON.stringify({ enabled: "true" })
  );
}

export function isAuthed(): boolean {
  return !!getLoginState();
}

export function isAdmin(): boolean {
  const state = getLoginState();
  return !!state && state.role == "ADMIN";
}

export function getLoginState(): LoginState | undefined {
  const token = window.sessionStorage.getItem("token");
  if (!!!token) {
    return undefined;
  }
  const decoded = jwtDecode<TokenValues>(token);
  const state: LoginState = {
    token: token,
    ...decoded,
  };
  return state;
}

// export function deletePost(id: Number, session?: Session) {
//   console.log(id);
// }
