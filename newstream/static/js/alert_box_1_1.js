function AlertBox( params ) {
    this.params = params || {};
    this.params.boxid = params.boxid || 'alert-wrapper';
    this.params.header_text = params.header_text || 'Operation Successful!';
    
    this.init();
}

AlertBox.prototype = {
    init: function() {
        this.instance = null;
        this.create();
        this.layout();
        this.actions();
    },
    create: function() {
        if( document.querySelector( '#'+this.params.boxid ) === null ) {
            var wrapper = document.createElement( "div" );
            wrapper.id = this.params.boxid;
            wrapper.classList.add('confirm-wrappers');
            var html = `<div id='confirm-box'><h4 id='confirm-header'>${this.params.header_text}</h4>`;
            html += "<div id='confirm-buttons'><button id='confirm-ok'>OK</button></div>";
            html += "</div>";
            
            wrapper.innerHTML = html;
            document.body.appendChild( wrapper );
        }
        
        this.instance = document.querySelector( '#'+this.params.boxid );
    },
    layout: function() {
        var wrapper = this.instance;
        var winHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;
        
        wrapper.style.height = winHeight + "px";	
    },
    show: function() {
        this.instance.style.display = "block";
        this.instance.style.opacity = 1;
    },
    hide: function( element ) {
        element.style.opacity = 0;
        setTimeout(function() {
            element.style.display = "none";
        }, 300);
    },
    actions: function() {
        var self = this;
        
        self.instance.querySelector( "#confirm-ok" ).
        addEventListener( "click", function() {
            self.hide( self.instance );
            setTimeout(function() {
                // remove confirm-wrapper to prevent listeners from registering more than once
                document.querySelector( '#'+self.params.boxid ).remove();
            }, 300);
        }, false);
    }
};

function nsAlert(message) {
    var alertBox = new AlertBox( {
        boxid: 'alert-box-id',
        header_text: message
    });
    alertBox.show();
}

// Usage:
// document.addEventListener( "DOMContentLoaded", function() {
//     var alert = document.querySelector( "#alert" );
//     var alertBox = new AlertBox( {
//         boxid: 'alert-box-id',
//         header_text: 'Some operation is done successfully!'
//     });
//     
//     alert.addEventListener( 'click', function() {
//         alertBox.show();
//     });
// });