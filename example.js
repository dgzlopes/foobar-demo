import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 1,
  duration: '10s',
};

export default function () {
  let res = http.get('http://127.0.0.1:8083/foo');
  check(res, {
    'is status 200': (r) => r.status === 200,
    'returns foobar': (r) => r.body == "foobar",
  });
  sleep(1);
}