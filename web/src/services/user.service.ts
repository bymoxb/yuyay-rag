import type { Response, User } from "../types";
import client from "./client";

export const getUserByEmail = async (): Promise<Response<User>> => {
  try {

    const { data } = await client.get("user");

    // console.log({ dataservice: data });

    return { ok: true, data: data.data };
  } catch (error) {
    return { ok: false, error: error instanceof Error ? error.message : 'Unknown error' };
  }
}
