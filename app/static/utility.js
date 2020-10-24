function posted_time_text(posted_date) {
    const time_now = new Date();
    let el_text = ""

    // Time since first calculated in hours 
    let time_since = Math.round((time_now - posted_date) / 36e5)

    // If time since (in hours) less than 1 use minutes instead
    if (time_since < 1) {
        time_since = Math.abs(Math.round(((time_now - posted_date) / 1000) / 60))
        el_text = `Posted ${time_since} minutes ago`
    
    // If time since in hours is greater than 24 swap to using days
    } else if (time_since > 24) {
    
        time_since = Math.ceil((time_now - posted_date) / (1000 * 60 * 60 * 24));
        
        if (time_since > 1) {
            el_text = `Posted ${time_since} days ago`
        } else {
            el_text = `Posted ${time_since} day ago`
        }
    
    // If hours between 1 & 24 continue and just use hours string
    } else {
        el_text = `Posted ${time_since} hours ago`
    }
    return el_text
}

function send_like_action(like_button) {
    
    const post_id = like_button.value
    const button_text = like_button.textContent

    const convert_obj = {Like: 'like', Unlike: 'unlike'}

    if (button_text == "Like") {
            like_button.textContent = "Unlike"
            like_button.classList.add("btn-outline-danger")
            like_button.classList.remove("btn-outline-success")
          } else {
            like_button.textContent = "Like"
            like_button.classList.add("btn-outline-success")
            like_button.classList.remove("btn-outline-danger")
          } 

    fetch(`/like/${post_id}/${convert_obj[button_text]}`)
    .then(response => {
      if (response.status !== 200) {
        console.log('Was not able to send like to server!')
        return;
      }

      response.json()
      .then(data => {
        if (data['result'] == true) {
        console.log("Updated")
          
          fetch_likes(post_id)
        }
      })      
    })
  } 

  function fetch_likes(post_id) {
    fetch(`/post/${post_id}/likes`)
    .then(response => {
      if (response.status !== 200) {
        console.log('Was not able to fetch post likes')
        return;
      }
      response.json()
      .then(data => {
        const var_div = document.getElementById('likes_div_'+post_id);
        let like_h6 = document.createElement("h6");

        if (data['like_number'] == 1) {
          like_h6.textContent = data['like_number'] + ' like';
        } else {
          like_h6.textContent = data['like_number'] + ' likes';
        }
        var_div.innerHTML = "";
        var_div.appendChild(like_h6);
      })

    })
  }
