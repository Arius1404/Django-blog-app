jQuery(document).ready(function ($) {

    $(function () {
        $('[data-toggle="tooltip"]').tooltip()
    })


    function delete_anchor() {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname
        if (location.includes('post')) {
            history.replaceState(null, null, location.replace("#start", ""))
        }
    }




    $('#navbarResponsive a').each(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        if (location.includes('category')) {
            $('a[href="/all_posts/"]').addClass('active')
        }
        let link = this.href;
        if (location == link) {
            $(this).parent().addClass('active');
        }
    });


    "use strict";


    // Page loading animation

    $(".preloader").animate({
        'opacity': '0'
    }, 600, function () {
        setTimeout(function () {
            $(".preloader").css("visibility", "hidden").fadeOut();
        }, 300);
    });


    $(window).scroll(function () {
        var scroll = $(window).scrollTop();
        var box = $('.header-text').height();
        var header = $('header').height();

        if (scroll >= 150) {
            $("header").addClass("background-header");
        } else {
            $("header").removeClass("background-header");
        }
    });

    if ($('.owl-clients').length) {
        $('.owl-clients').owlCarousel({
            loop: true,
            nav: false,
            dots: true,
            items: 1,
            margin: 30,
            autoplay: false,
            smartSpeed: 700,
            autoplayTimeout: 6000,
            responsive: {
                0: {
                    items: 1,
                    margin: 0
                },
                460: {
                    items: 1,
                    margin: 0
                },
                576: {
                    items: 3,
                    margin: 20
                },
                992: {
                    items: 5,
                    margin: 30
                }
            }
        });
    }

    if ($('.owl-banner').length) {
        $('.owl-banner').owlCarousel({
            loop: true,
            nav: true,
            dots: true,
            items: 3,
            margin: 10,
            autoplay: false,
            smartSpeed: 700,
            autoplayTimeout: 6000,
            responsive: {
                0: {
                    items: 1,
                    margin: 0
                },
                460: {
                    items: 1,
                    margin: 0
                },
                576: {
                    items: 1,
                    margin: 10
                },
                992: {
                    items: 3,
                    margin: 10
                }
            }
        });
    }


    $(document).ready(function () {
        let location = window.location.protocol + '//' + window.location.host + window.location.pathname;
        if (location.includes('post') && !location){
            setTimeout(delete_anchor, 1000)
        }
        if (location.includes('create') || (location.includes('edit'))){
            $("#cat-select").prepend(new Option());
        $('.js-example-basic-single').select2({
            placeholder: "Выберите категорию поста",
            allowClear: true
        });
        if(location.includes('create')){
            $('#cat-select').val(null).trigger('change');
        }
        $('#tag-select-field').select2({
            placeholder: "Отметьте необходимые теги",
            allowClear: true
        }).focus(function () {
            $(this).select2('focus');
        });


        $('#tag-select-field').on('select2:opening select2:closing', function (event) {
            var $searchfield = $(this).parent().find('.select2-search__field');
            $searchfield.prop('disabled', true);
        });
        }
    });

});
