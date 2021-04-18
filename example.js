import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 5,
  duration: '30s',
};

export default function () {
  let res = http.get('http://foo:5000/foo');
  check(res, {
    'is status 200': (r) => r.status === 200,
    'returns foobar': (r) => r.body == "foobar",
  });
  sleep(1);
}