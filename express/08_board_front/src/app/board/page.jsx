"use client";
import {useEffect, useState} from "react";
import api from "@/app/lib/api";

export default function Board() {
    const [list, setList] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const res = await api.get("/board/list/1");
                console.log("res 데이터 : ", res.data);

                if (res.data.success) {
                    setList(res.data.list);
                }
            } catch (e) {
                console.error("에러발생 :", e);
            }
        }

        fetchData();
    }, []);

    return (
        <div>
            <h1>게시판</h1>
            <ul>
                {list.map((item) => (
                <li key={item.idx}>
                    {item.subject} - {item.user_name}
                </li>
            ))}
            </ul>
        </div>
    );
}