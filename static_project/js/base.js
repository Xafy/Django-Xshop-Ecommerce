$(document).ready(function(){

    //contact-form handler
    var contactForm = $(".contact-form")
    var contactFormMethod = contactForm.attr("method")
    var contactFormEndPoint = contactForm.attr("action")
    var thisForm = $(this)

    contactForm.submit(function(event){
        event.preventDefault()
        var contactFormData = contactForm.serialize()
        $.ajax({
            method : contactFormMethod,
            url : contactFormEndPoint,
            data : contactFormData,
            success: function(data){
                contactForm[0].reset()
                $.alert({
                    title:"success",
                    content:data.message,
                    theme:"modern"
                })
            },
            error: function(error){
                console.log(error.responseJSON)
                var jsonData = error.responseJSON
                var msg  = ""

                $.each(jsonData, function(key, value){
                    msg += key + " : " + value[0].message + "<br/>"
                })
                console.log(msg)
                $.alert({
                    title:"somthing went wrong",
                    content:msg,
                    theme:"modern"
                })
            }
        })
    })

    //add-remove from cart
    var productForm = $(".form-product-ajax")

    productForm.submit(function(event){
        event.preventDefault();
        var thisForm = $(this);
        // var actionEndpoint = thisForm.attr("action");
        var actionEndpoint = thisForm.attr('data-endpoint')
        var httpMethod = thisForm.attr("method");
        var formData = thisForm.serialize();

        $.ajax({
            url : actionEndpoint,
            method : httpMethod,
            data : formData,
            success : function(data){
                var submitSpan = thisForm.find(".submit-span")
                if (data.added){
                    submitSpan.html("<button type='submit' class ='btn btn-danger'>Remove from cart</button>")
                }
                else
                {
                    submitSpan.html("<button type='submit' class ='btn btn-success'>ADD to cart</button>")
                }
                
                var navbarCount = $(".cart-count")
                navbarCount.text(data.cartCount) 

                var currentPath = window.location.href
                if (currentPath.indexOf("cart") != -1)
                {
                    refreshCart()
                }
            },
            error: function(errorData){
                console.log("Error")
                console.log(errorData)
            }

        })
    })

    // cart home refresh
    function refreshCart(){
        console.log('in current cart')
        var cartTable = $(".cart-table")
        var cartBody = cartTable.find(".cart-body")
        var productRows = cartBody.find(".cart-product")
        var cartSubtotal = cartBody.find(".cart-subtotal")
        var cartTotal = cartBody.find(".cart-total")
        var currentUrl = window.location.href
        var refreshCartUrl = '/api/cart/';
        var refreshCartMethod = 'GET';
        var data = {};

        $.ajax({
            url : refreshCartUrl,
            method : refreshCartMethod,
            data : data,
            success: function(data){
                var hiddenCartItemRemoveForm = $(".cart-item-remove-form")
                if (data.products.length > 0){
                        productRows.html("")
                        i = data.products.length
                        $.each(data.products, function(index, value){
                            var newCartItemRemove = hiddenCartItemRemoveForm.clone()
                            newCartItemRemove.css("display", "block")
                            // newCartItemRemove.removeClass("hidden-class")
                            newCartItemRemove.find(".cart-item-product-id").val(value.id)
                            cartBody.prepend("<tr><th scope=\"row\">"+i+"</th><td><a href='"+value.url+"'>"+value.title+"</a>" + newCartItemRemove.html() + "</td><td>"+ value.price +"</td></tr>")
                            i--
                        })
                        cartSubtotal.text(data.subtotal)
                        cartTotal.text(data.total)
                        currentUrl = currentUrl
                }
            },
            error: function(errorData){
                console.log("Error refresh")
                console.log(errorData)
            }
        })
    }
})