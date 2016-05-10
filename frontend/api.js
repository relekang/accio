import Cookies from 'js-cookie';
import bluebird from 'bluebird';
import request from 'superagent';

bluebird.promisifyAll(request);

const headers = Object.freeze({
  Accept: 'application/json',
  'Content-Type': 'application/json',
  'X-CSRFToken': Cookies.get('csrftoken'),
});

const extractBody = response => response.body;

export const get = (path, data) => {
  const url = data && data.id ? `/api${path}/${data.id}/` : `/api${path}/`;
  return request
    .get(url)
    .set(headers)
    .endAsync()
    .then(extractBody)
    .then(response => {
      if (response.results) {
        return response.results;
      }
      return response;
    });
};

export const add = (path, data) => request
  .post(`/api${path}/`)
  .set(headers)
  .send(JSON.stringify(data))
  .endAsync()
  .then(extractBody);

export const save = (path, data) => request
  .put(`/api${path}/${data.id}/`)
  .set(headers)
  .send(JSON.stringify(data))
  .endAsync()
  .then(extractBody);

export const update = (path, data) => request
  .patch(`/api${path}/${data.id}/`)
  .set(headers)
  .send(JSON.stringify(data))
  .endAsync()
  .then(extractBody);

export const remove = (path, data) => request
  .delete(`/api${path}/${data.id}/`)
  .set(headers)
  .endAsync()
  .then(extractBody);
