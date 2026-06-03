import http from "k6/http";
import { check } from "k6";

export const options = {
    vus:2000,
    duration: "30s",
};

export default function () {
    const response = http.get(
        "http://web:8000/GEcZAa/", {redirects: 0}
    );

    check(response, {
        "status is redirect": (r) =>
            r.status === 301 || r.status === 302,
    });
}