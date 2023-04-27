function ConfirmBox( params ) {
    this.params = params || {};
    this.params.boxid = params.boxid || 'confirm-wrapper';
    this.params.header_text = params.header_text || 'Are you sure?';
    this.params.ok = params.ok || function() {};
    this.params.cancel = params.cancel || function() {};
    
    this.init();
}

ConfirmBox.prototype = {
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
            html += "<div id='confirm-buttons'><button id='confirm-ok'>Confirm</button><button type='button' id='confirm-cancel'>Cancel</button></div>";
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
                self.params.ok();
                // remove confirm-wrapper to prevent listeners from registering more than once
                document.querySelector( '#'+self.params.boxid ).remove();
            }, 300);
        }, false);
        
        
        self.instance.querySelector( "#confirm-cancel" ).
        addEventListener( "click", function() {
            self.hide( self.instance );
            setTimeout(function() {
                self.params.cancel();
                // remove confirm-wrapper to prevent listeners from registering more than once
                document.querySelector( '#'+self.params.boxid ).remove();
            }, 300);
        }, false);
    }
};

// Usage:
// document.addEventListener( "DOMContentLoaded", function() {
//     var confirm = document.querySelector( "#confirm" );
//     var output = document.querySelector( "#output" );
//     var confBox = new ConfirmBox( {
//         boxid: 'confirm-box-id',
//         header_text: 'Are you sure you want to do this?',
//         ok: function() {
//             output.innerHTML = "OK";
//         },
//         cancel: function() {
//             output.innerHTML = "Cancel";
//         }
//     });
//     
//     confirm.addEventListener( 'click', function() {
//         confBox.show();
//     });
// });