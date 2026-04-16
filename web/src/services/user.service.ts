import client from "./client";

type Response<T> = {
  ok: true,
  data: T,
} | {
  ok: false,
  error: string,
}

type User = {
  email: string,
  fullName: string,
  roles: string[],
  functionalities: string[],
}

export const getUserByEmail = async (): Promise<Response<User>> => {
  try {

    const { data } = await client.get("user");

    // console.log({ dataservice: data });

    return { ok: true, data: data.data };
  } catch (error) {
    return { ok: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
}
