export default function ({ $axios, app, store}) {
    $axios.onRequest(config => {
          config.headers.common["Authorization"] = "Bearer " + store.state.user.token
    });
    $axios.onResponse(response => {

    })
    $axios.onError(error => {
        if(error.response.status === 403) {

        }
        if(error.response.status === 401) {

        }
    });
}
