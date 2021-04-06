export default function ({ $axios, app, store}) {
    $axios.onRequest(config => {
          config.headers.common["Authorization"] = "Bearer " + store.state.user.token
    });
    $axios.onResponse(response => {

    })
    $axios.onError(error => {
        if(error.response.status === 403) {
          store.commit("LOGOUT")
        }
        if(error.response.status === 401) {
          store.commit("LOGOUT")
        }
    });
}
