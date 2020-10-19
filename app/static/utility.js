
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
