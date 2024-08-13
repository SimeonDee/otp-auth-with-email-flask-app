timer_display_div = document.getElementById('timer-display-div')

verify_otp_btn = document.getElementById('verify-otp-btn')

let OTP
let timer = 0
let timerId = null

function stopTimer(id){
    clearInterval(id)
}

async function startTimer(countdown_max){
    timer = Number.parseInt(countdown_max)

    timerId = setInterval(()=>{
        minute = Math.trunc(timer / 60)
        seconds = timer % 60

        minStr = String(minute).padStart(2, '0')
        secStr = String(seconds).padStart(2, '0')

        timer_display_div.innerHTML = `<b>${minStr}:${secStr}</b>`

        timer--

        if(timer <= 0){
            stopTimer(timerId)
            timerId=null
            timer=0
            verify_otp_btn.enabled = false
        }
    }, 1000)
}

verify_otp_btn.addEventListener('submit', (e, id)=>{
    if (id){
        stopTimer(id)
        timer = 0
        timerId = null
        timer_display_div.innerHTML = '<b>00:00</b>'

    }
})