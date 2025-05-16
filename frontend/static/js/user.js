function get_user_query(){
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get('nickname');	
}