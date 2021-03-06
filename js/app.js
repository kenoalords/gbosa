import jQuery from "jquery";
import Quill from "quill";
import autoResize from "autoresize-textarea";
import '../scss/main.scss';

//  tagSuggestions
!function(a){a.fn.inputTags=function(b){if("inputTags"in window||(window.inputTags={instances:[]}),window.inputTags.methods={tags:function(a,b){if(a){switch(typeof a){case"string":switch(a){case"_toString":var c=d.tags.toString();return b?b(c):c;case"_toObject":var e=d._toObject(d.tags);return b?b(e):e;case"_toJSON":var e=d._toObject(d.tags),f=JSON.stringify(e);return b?b(f):f;case"_toArray":return b?b(d.tags):d.tags}var g=a.split(",");if(g.length>1){var h=d.tags;d.tags=h.concat(g)}else d.tags.push(g[0]);break;case"object":var h=d.tags;"[object Object]"===Object.prototype.toString.call(a)&&(a=Object.keys(a).map(function(b){return a[b]})),d.tags=h.concat(a);break;case"function":return a(d.tags)}if(d._clean(),d._fill(),d._updateValue(),d.destroy(),d._setInstance(d),b)return b(d.tags)}return d.tags},event:function(a,b){d.options[a]=b,d._setInstance(d)},options:function(a,b){return a||b?b?(d.options[a]=b,void d._setInstance(d)):d.options[a]:d.options},destroy:function(){var b=a(this).attr("data-uniqid");delete window.inputTags.instances[b]}},"object"==typeof b||!b){var b=a.extend(!0,{},a.fn.inputTags.defaults,b);this.each(function(){var c=a(this);c.UNIQID=Math.round(Date.now()/(494*Math.random()-54)),c.DEFAULT_CLASS="inputTags",c.ELEMENT_CLASS=c.DEFAULT_CLASS+"-"+c.UNIQID,c.LIST_CLASS=c.DEFAULT_CLASS+"-list",c.ITEM_CLASS=c.DEFAULT_CLASS+"-item",c.ITEM_CONTENT='<span class="value" title="Cliquez pour éditer">%s</span><i class="close-item">&times</i>',c.FIELD_CLASS=c.DEFAULT_CLASS+"-field",c.ERROR_CLASS=c.DEFAULT_CLASS+"-error",c.ERROR_CONTENT='<p class="'+c.ERROR_CLASS+'">%s</p>',c.AUTOCOMPLETE_LIST_CLASS=c.DEFAULT_CLASS+"-autocomplete-list",c.AUTOCOMPLETE_ITEM_CLASS=c.DEFAULT_CLASS+"-autocomplete-item",c.AUTOCOMPLETE_ITEM_CONTENT='<li class="'+c.AUTOCOMPLETE_ITEM_CLASS+'">%s</li>',c.options=b,c.keys=[13,188,27],c.tags=[],c.options.keys.length>0&&(c.keys=c.keys.concat(c.options.keys)),c.init=function(){c.addClass(c.ELEMENT_CLASS).attr("data-uniqid",c.UNIQID),c.$element=a("."+c.ELEMENT_CLASS),c.$element.hide(),c.build(),c.fill(),c.save(),c.edit(),c.destroy(),c._autocomplete()._init(),c._focus()},c.build=function(){c.$html=a("<div>").addClass(c.LIST_CLASS),c.$input=a("<input>").attr({type:"text",class:c.FIELD_CLASS}),c.$html.insertAfter(c.$element).prepend(c.$input),c.$list=c.$element.next("."+c.LIST_CLASS),c.$list.on("click",function(b){return!a(b.target).hasClass("inputTags-field")&&void c.$input.focus()})},c.fill=function(){return c._getDefaultValues(),0!==c.options.tags&&(c._concatenate(),c._updateValue(),void c._fill())},c._fill=function(){c.tags.forEach(function(a,b){var d=c._validate(a,!1);(!0===d||"max"===d&&b+1<=c.options.max)&&c._buildItem(a)})},c._clean=function(){a("."+c.ITEM_CLASS,c.$list).remove()},c.save=function(){c.$input.on("keyup",function(b){b.preventDefault();var d=b.keyCode||b.which,e=c.$input.val().trim();if(a.inArray(d,c.keys)<0)return!1;if(27===d)return c._cancel(),!1;if(e=188===d?e.slice(0,-1):e,!c._validate(e,!0))return!1;if(c.options.only&&c._exists(e))return c._errors("exists"),!1;if(c.$input.hasClass("is-edit")){var f=c.$input.attr("data-old-value");if(f===e)return c._cancel(),!0;c._update(f,e),c._clean(),c._fill()}else{if(c._autocomplete()._isSet()&&c._autocomplete()._get("only")&&a.inArray(e,c._autocomplete()._get("values"))<0)return c._autocomplete()._hide(),c._errors("autocomplete_only"),!1;if(c._exists(e)){c.$input.removeClass("is-autocomplete"),c._errors("exists");var g=a('[data-tag="'+e+'"]',c.$list);return g.addClass("is-exists"),setTimeout(function(){g.removeClass("is-exists")},300),!1}c._buildItem(e),c._insert(e)}return c._cancel(),c._updateValue(),c.destroy(),c._autocomplete()._build(),c._setInstance(c),c.$input.focus(),!1})},c.edit=function(){c.$list.on("click","."+c.ITEM_CLASS,function(b){if(a(b.target).hasClass("close-item")||!1===c.options.editable||c._autocomplete()._isSet()&&c._autocomplete()._get("only"))return c._cancel(),!0;var d=a(this).addClass("is-edit"),e=a(".value",d).text();c.$input.width(d.outerWidth()).insertAfter(d).addClass("is-edit").attr("data-old-value",e).val(e).focus(),c._bindEvent("selected"),c.$input.on("blur",function(){c._cancel(),c._bindEvent("unselected")})})},c.destroy=function(){a("."+c.ITEM_CLASS,c.$list).off("click").on("click",".close-item",function(){var b=a(this).parent("."+c.ITEM_CLASS),d=a(".value",b).text();b.addClass("is-closed"),setTimeout(function(){c._pop(d),c._updateValue(),b.remove(),c._autocomplete()._build(),c.$input.focus(),c._setInstance(c)},200)})},c._buildItem=function(b){var d=a(c.ITEM_CONTENT.replace("%s",b)),e=a("<span>").addClass(c.ITEM_CLASS+" is-closed").attr("data-tag",b).html(d);e.insertBefore(c.$input).delay(100).queue(function(){a(this).removeClass("is-closed")})},c._getIndex=function(a){return c.tags.indexOf(a)},c._concatenate=function(){(!1===typeof c.options.max||c.options.max>0)&&c.options.tags.length>c.options.max&&c.options.tags.splice(-Math.abs(c.options.tags.length-c.options.max)),c.tags=c.tags.concat(c.options.tags)},c._getDefaultValues=function(){c.$element.val().length>0?c.tags=c.tags.concat(c.$element.val().split(",")):c.$element.attr("value","")},c._insert=function(a){c.tags.push(a),c._bindEvent(["change","create"])},c._update=function(a,b){var d=c._getIndex(a);c.tags[d]=b,c._bindEvent(["change","update"])},c._pop=function(a){var b=c._getIndex(a);return!(b<0)&&(c.tags.splice(b,1),void c._bindEvent(["change","destroy"]))},c._cancel=function(){a("."+c.ITEM_CLASS).removeClass("is-edit"),c.$input.removeClass("is-edit is-autocomplete").removeAttr("data-old-value style").val("").appendTo(c.$list)},c._autocomplete=function(){var b=c.options.autocomplete.values;return{_isSet:function(){return b.length>0},_init:function(){return!!c._autocomplete()._isSet()&&void c._autocomplete()._build()},_build:function(){c._autocomplete()._exists()&&c.$autocomplete.remove(),c.$autocomplete=a("<ul>").addClass(c.AUTOCOMPLETE_LIST_CLASS),c._autocomplete()._get("values").forEach(function(b,d){var e=c.AUTOCOMPLETE_ITEM_CONTENT.replace("%s",b),f=a.inArray(b,c.tags)>=0?a(e).addClass("is-disabled"):a(e);f.appendTo(c.$autocomplete)}),c._autocomplete()._bindClick(),a(document).not(c.$autocomplete).on("click",function(){c._autocomplete()._hide()})},_bindClick:function(){a(c.$autocomplete).off("click").on("click","."+c.AUTOCOMPLETE_ITEM_CLASS,function(b){if(a(b.target).hasClass("is-disabled"))return!1;c.$input.addClass("is-autocomplete").val(a(this).text()),c._autocomplete()._hide(),c._bindEvent("autocompleteTagSelect");var b=a.Event("keyup");b.which=13,c.$input.trigger(b)})},_show:function(){return!!c._autocomplete()._isSet()&&(c.$autocomplete.css({left:c.$input[0].offsetLeft,minWidth:c.$input.width()}).insertAfter(c.$input),void setTimeout(function(){c._autocomplete()._bindClick(),c.$autocomplete.addClass("is-active")},100))},_hide:function(){c.$autocomplete.removeClass("is-active")},_get:function(a){return c.options.autocomplete[a]},_exists:function(){return void 0!==c.$autocomplete}}},c._updateValue=function(){c.$element.attr("value",c.tags.join(","))},c._focus=function(){c.$input.on("focus",function(){c._bindEvent("focus"),!c._autocomplete()._isSet()||c.$input.hasClass("is-autocomplete")||c.$input.hasClass("is-edit")||c._autocomplete()._show()})},c._toObject=function(a){return a.reduce(function(a,b,c){return a[c]=b,a},{})},c._validate=function(a,b){var d,e="";switch(!0){case!a:case void 0===a:case 0===a.length:c._cancel(),e="empty";break;case a.length>0&&a.length<c.options.minLength:e="minLength";break;case a.length>c.options.maxLength:e="maxLength";break;case c.options.max>0&&c.tags.length>=c.options.max:c.$input.hasClass("is-edit")||(e="max");break;case c.options.email:d=/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/,d.test(a)||(e="email")}return!(e.length>0)||(b?c._errors(e):e)},c._exists=function(b){return a.inArray(b,c.tags)>=0},c._errors=function(a){return 0!==a.length&&(c._autocomplete()._exists()&&c.$autocomplete.remove(),c._displayErrors(c.options.errors[a].replace("%s",c.options[a]),a),!1)},c._displayErrors=function(b,d){var e=a(c.ERROR_CONTENT.replace("%s",b)).attr("data-error",d),f=c.options.errors.timeout;return!a("."+c.ERROR_CLASS+'[data-error="'+d+'"]').length&&(e.hide().insertAfter(c.$list).slideDown(),!(!f||f<=0)&&(a("."+c.ERROR_CLASS).on("click",function(){c._collapseErrors(a(this))}),void setTimeout(function(){c._collapseErrors()},f)))},c._collapseErrors=function(b){var d=b?b:a("."+c.ERROR_CLASS);d.slideUp(300,function(){d.remove()})},c._getInstance=function(){return window.inputTags.instances[c.UNIQID]},c._setInstance=function(a){window.inputTags.instances[c.UNIQID]=c},c._isSet=function(a){return!(void 0===c.options[a]||!1===c.options[a]||c.options[a].length<=0)},c._callMethod=function(a,b){return void 0!==b.options[a]&&"function"==typeof b.options[a]&&void b.options[a].apply(this,Array.prototype.slice.call(arguments,1))},c._initEvent=function(a,b){if(!a)return!1;switch(typeof a){case"string":b(a,c);break;case"object":a.forEach(function(a,d){b(a,c)})}return!0},c._bindEvent=function(a){return c._initEvent(a,function(a,b){c._callMethod(a,b)})},c._unbindEvent=function(a){return c._initEvent(a,function(a,b){c.options[a]=!1})},c.init(),c._bindEvent("init"),c._setInstance(c)});return{on:function(a,b){window.inputTags.methods.event(a,b)}}}if(window.inputTags.methods[b]){var c=a(this).attr("data-uniqid"),d=window.inputTags.instances[c];return void 0===d?a.error("[undefined instance] No inputTags instance found."):window.inputTags.methods[b].apply(this,Array.prototype.slice.call(arguments,1))}a.error("[undefined method] The method ["+b+"] does not exists.")},a.fn.inputTags.defaults={tags:[],keys:[],minLength:2,maxLength:30,max:6,email:!1,only:!0,init:!1,create:!1,update:!1,destroy:!1,focus:!1,selected:!1,unselected:!1,change:!1,autocompleteTagSelect:!1,editable:!0,autocomplete:{values:[],only:!1},errors:{empty:"Attention, vous ne pouvez pas ajouter un tag vide.",minLength:"Attention, votre tag doit avoir au minimum %s caractères.",maxLength:"Attention, votre tag ne doit pas dépasser %s caractères.",max:"Attention, le nombre de tags ne doit pas dépasser %s.",email:"Attention, l'adresse email que vous avez entré n'est pas valide",exists:"Attention, ce tag existe déjà !",autocomplete_only:"Attention, vous devez sélectionner une valeur dans la liste.",timeout:8e3}}}(jQuery);


// if ( 'serviceWorker' in navigator ){
// 	navigator.serviceWorker.register('/sw.js').then((reg)=>{
// 		console.log('Service worker registered!');
// 	}).catch((err)=>{
// 		console.log('Service worker registration failed');
// 	})
// }

class TextEditor {
    constructor(el, button){
        try{
            this.el = document.querySelector(el);
            this.innerEditor = null;
            this.setUpEditor(this.el)
            if ( this.el.value.length > 10 ){
                document.querySelector('.ql-editor').innerHTML = this.el.value
            }
        } catch (e) {
            console.log('Oops! editor not found')
        }
    }

    setUpEditor(el){
        let parent = el.parentNode
        let editor_wrapper = document.createElement('div');
        // Setup wrapper
        editor_wrapper.setAttribute('id', 'editor-wrapper')
        parent.appendChild(editor_wrapper)
        const editor = this.initEditor(editor_wrapper)
        if(editor){
            el.style.display = 'none';
            let form = parent.closest('form');
            let button = form.querySelector('#submit-post-button');
            this.innerEditor = parent.querySelector('.ql-editor');
            button.addEventListener('click', (e)=>{
                this.submitButtonClicked(editor)
            })
        }
    }

    submitButtonClicked(editor){
        this.el.value = this.innerEditor.innerHTML;
    }

    initEditor(wrapper){
        return new Quill(wrapper, {
            theme: 'snow'
        })
    }
}
const description = new TextEditor('#id_description');
const answer = new TextEditor('#id_answer');
var resizeTextarea = jQuery('.is-auto-resize').autoResize()

const PostType = {
    editor: null,
    defPost: jQuery('.def-post'),
    init: function(el, editor){
        this.editor = editor;
        let value = jQuery(`${el} option:selected`).text()
        this.manipulateForm(value.toLowerCase())

        jQuery(el).on('change', function(e){
            let option = jQuery(`${el} option:selected`).text()
            PostType.manipulateForm(option.toLowerCase())
        })
    },
    manipulateForm: function(value){
        switch (value) {
            case 'question':
                this.hideEditor();
                jQuery('#id_title').attr('placeholder', 'Start your question with What, How, Where, Why etc.')
                this.defPost.html('question')
                break;
            case 'experience':
                this.showEditor();
                this.defPost.html('experience')
                jQuery('#id_title').attr('placeholder', 'Enter a title')
                break;
            default:
                break;
        }
    },
    showEditor: function(){
        jQuery(this.editor).slideDown('fast')
    },
    hideEditor: function(){
        jQuery(this.editor).slideUp('fast')
    }
}

try{
	if(jQuery('#id_tags').length > 0){
		jQuery('#id_tags').inputTags();
	}
} catch (e){
    console.log(e.message);
}

jQuery('#menu-trigger').on('click', (e)=>{
	e.preventDefault();
	jQuery('#main-navbar').find('.navbar-menu').toggleClass('is-active');
	jQuery('#menu-trigger').toggleClass('is-active');
})

PostType.init('#id_post_type', '#description')

const SidebarMenu = {
	init: function(el){
		jQuery(el).on('click', function(e){
			e.preventDefault();
			SidebarMenu.openMenu();
		});
	},
	openMenu: function(){
		jQuery('body').addClass('sidebar-menu-active')
	},
	closeMenu: function(){
		jQuery('body').removeClass('sidebar-menu-active')
	}
}

SidebarMenu.init("#sidebar-menu-trigger");

jQuery('#sidebar-menu').on('click', function(e){
	if ( e.target === this){
		SidebarMenu.closeMenu();
	}
});

jQuery('#close-menu').on('click', function(e){
	e.preventDefault()
	SidebarMenu.closeMenu();
})
