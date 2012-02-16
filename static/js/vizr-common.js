var flash_error = function(parent, error) {
    var el = $('<p class="error">' + error + '</p>');
    el.css('display', 'none');
    el.css('opacity', '0');
    parent.append(el);

    el.slideDown(200);
    el.animate({opacity:1}, 100);

    el.delay(3000).animate({opacity:0}, 2000).slideUp(100, function() {el.remove()});
};

var flash_msg = function(parent, msg, cat) {
    if (cat == null) { cat='msg';}
    var el = $('<div class="alert-message warning">' + msg + '</div>');
    el.css('display', 'none');
    el.css('opacity', '0');
    parent.append(el);

    el.slideDown(200);
    el.animate({opacity:1}, 100);

    el.delay(3000).animate({opacity:0}, 2000).slideUp(100, function() {el.remove()});
};


var jpost = function(url, data, callback) {
    data['csrf'] = $('#csrf').val();//grab the hidden csrf token
    $.post( url , data , function(resp){
        $('#csrf').val(resp.meta.csrf);//reset the csrf token
        if (resp.meta.flash) {
            $.each(resp.meta.flash, function(index) {
                var m = resp.meta.flash[index];
                flash_msg($('#messages'), m.msg, m.cat);
            });
        }
        callback(resp);}, 'json');
};

