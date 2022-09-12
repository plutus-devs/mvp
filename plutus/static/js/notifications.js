const notiListDiv = document.querySelector("#notiListDiv");
const numNotiSpan = document.querySelector("#numNotiSpan");
const notificationURL = "/notifications/get_notifications/";


function get_notifications() {
    notiListDiv.innerHTML = ""
    numNotiSpan.innerHTML = ""
    var url_params = "/notifications/get_notifications/"
    var requestOptions = {
        method: 'GET',
        redirect: 'follow'
    };

    fetch(url_params, requestOptions)
        .then(response => response.json())
        .then(result => {
            var notifications = result["message"]["notifications"]
            if (notifications.length > 0) {
                numNotiSpan.innerHTML = `+${notifications.length}`;
                numNotiSpan.style.display = "block";
                notifications.forEach(noti => {
                    var div = `
                    <div class="card mt-2">
                        <div class="card-body">
                            <h5 class="card-title">${noti.title}</h5>
                            <p class="card-text">
                                ${noti.message}
                            </p>

                            <a href="${noti.url}" class="stretched-link" style="color: inherit;text-decoration: inherit;">${noti.time}</a>
                        </div>
                    </div>
                    `;
                    notiListDiv.innerHTML += div;
                });
            } else {
                numNotiSpan.style.display = "none";
                notiListDiv.innerHTML += "<div class='text-center'>ไม่พบข้อมูล</div>";
            }


        })
};

get_notifications();
setInterval(() => {
    get_notifications();
}, 1000 * 30);
