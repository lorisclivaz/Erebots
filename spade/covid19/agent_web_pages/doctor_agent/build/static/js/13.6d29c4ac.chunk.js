(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[13],{568:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={tag:u.q,inverse:c.a.bool,color:c.a.string,body:c.a.bool,outline:c.a.bool,className:c.a.string,cssModule:c.a.object,innerRef:c.a.oneOfType([c.a.object,c.a.string,c.a.func])},f=function(e){var t=e.className,a=e.cssModule,o=e.color,i=e.body,c=e.inverse,l=e.outline,p=e.tag,f=e.innerRef,b=Object(s.a)(e,["className","cssModule","color","body","inverse","outline","tag","innerRef"]),m=Object(u.m)(d()(t,"card",!!c&&"text-white",!!i&&"card-body",!!o&&(l?"border":"bg")+"-"+o),a);return r.a.createElement(p,Object(n.a)({},b,{className:m,ref:f}))};f.propTypes=p,f.defaultProps={tag:"div"},t.a=f},569:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={tag:u.q,className:c.a.string,cssModule:c.a.object,innerRef:c.a.oneOfType([c.a.object,c.a.string,c.a.func])},f=function(e){var t=e.className,a=e.cssModule,o=e.innerRef,i=e.tag,c=Object(s.a)(e,["className","cssModule","innerRef","tag"]),l=Object(u.m)(d()(t,"card-body"),a);return r.a.createElement(i,Object(n.a)({},c,{className:l,ref:o}))};f.propTypes=p,f.defaultProps={tag:"div"},t.a=f},570:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p=c.a.oneOfType([c.a.number,c.a.string]),f={tag:u.q,noGutters:c.a.bool,className:c.a.string,cssModule:c.a.object,form:c.a.bool,xs:p,sm:p,md:p,lg:p,xl:p},b={tag:"div",widths:["xs","sm","md","lg","xl"]},m=function(e){var t=e.className,a=e.cssModule,o=e.noGutters,i=e.tag,c=e.form,l=e.widths,p=Object(s.a)(e,["className","cssModule","noGutters","tag","form","widths"]),f=[];l.forEach((function(t,a){var n=e[t];if(delete p[t],n){var s=!a;f.push(s?"row-cols-"+n:"row-cols-"+t+"-"+n)}}));var b=Object(u.m)(d()(t,o?"no-gutters":null,c?"form-row":"row",f),a);return r.a.createElement(i,Object(n.a)({},p,{className:b}))};m.propTypes=f,m.defaultProps=b,t.a=m},571:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p=c.a.oneOfType([c.a.number,c.a.string]),f=c.a.oneOfType([c.a.bool,c.a.number,c.a.string,c.a.shape({size:c.a.oneOfType([c.a.bool,c.a.number,c.a.string]),order:p,offset:p})]),b={tag:u.q,xs:f,sm:f,md:f,lg:f,xl:f,className:c.a.string,cssModule:c.a.object,widths:c.a.array},m={tag:"div",widths:["xs","sm","md","lg","xl"]},h=function(e,t,a){return!0===a||""===a?e?"col":"col-"+t:"auto"===a?e?"col-auto":"col-"+t+"-auto":e?"col-"+a:"col-"+t+"-"+a},g=function(e){var t=e.className,a=e.cssModule,o=e.widths,i=e.tag,c=Object(s.a)(e,["className","cssModule","widths","tag"]),l=[];o.forEach((function(t,n){var s=e[t];if(delete c[t],s||""===s){var o=!n;if(Object(u.k)(s)){var r,i=o?"-":"-"+t+"-",p=h(o,t,s.size);l.push(Object(u.m)(d()(((r={})[p]=s.size||""===s.size,r["order"+i+s.order]=s.order||0===s.order,r["offset"+i+s.offset]=s.offset||0===s.offset,r)),a))}else{var f=h(o,t,s);l.push(f)}}})),l.length||l.push("col");var p=Object(u.m)(d()(t,l),a);return r.a.createElement(i,Object(n.a)({},c,{className:p}))};g.propTypes=b,g.defaultProps=m,t.a=g},572:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={tag:u.q,className:c.a.string,cssModule:c.a.object},f=function(e){var t=e.className,a=e.cssModule,o=e.tag,i=Object(s.a)(e,["className","cssModule","tag"]),c=Object(u.m)(d()(t,"card-header"),a);return r.a.createElement(o,Object(n.a)({},i,{className:c}))};f.propTypes=p,f.defaultProps={tag:"div"},t.a=f},588:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={tag:u.q,className:c.a.string,cssModule:c.a.object},f=function(e){var t=e.className,a=e.cssModule,o=e.tag,i=Object(s.a)(e,["className","cssModule","tag"]),c=Object(u.m)(d()(t,"input-group-text"),a);return r.a.createElement(o,Object(n.a)({},i,{className:c}))};f.propTypes=p,f.defaultProps={tag:"span"},t.a=f},590:function(e,t,a){"use strict";a.d(t,"a",(function(){return g}));var n=a(573),s=a.n(n),o=a(576),r=a.n(o),i=a(579),c=a.n(i),l=a(581),d=a.n(l),u=a(1),p=a(586),f=a.n(p),b=a(585),m=a(589),h=function(e){function t(){for(var t,a=arguments.length,n=new Array(a),s=0;s<a;s++)n[s]=arguments[s];return t=e.call.apply(e,[this].concat(n))||this,d()(r()(t),"refHandler",(function(e){Object(m.b)(t.props.innerRef,e),Object(m.a)(t.props.setReferenceNode,e)})),t}c()(t,e);var a=t.prototype;return a.componentWillUnmount=function(){Object(m.b)(this.props.innerRef,null)},a.render=function(){return f()(Boolean(this.props.setReferenceNode),"`Reference` should not be used outside of a `Manager` component."),Object(m.c)(this.props.children)({ref:this.refHandler})},t}(u.Component);function g(e){return u.createElement(b.b.Consumer,null,(function(t){return u.createElement(h,s()({setReferenceNode:t},e))}))}},593:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(566),r=a(35),i=a(1),c=a.n(i),l=a(6),d=a.n(l),u=a(84),p=a.n(u),f=a(40),b={children:d.a.node,type:d.a.string,size:d.a.string,bsSize:d.a.string,valid:d.a.bool,invalid:d.a.bool,tag:f.q,innerRef:d.a.oneOfType([d.a.object,d.a.func,d.a.string]),plaintext:d.a.bool,addon:d.a.bool,className:d.a.string,cssModule:d.a.object},m=function(e){function t(t){var a;return(a=e.call(this,t)||this).getRef=a.getRef.bind(Object(o.a)(a)),a.focus=a.focus.bind(Object(o.a)(a)),a}Object(r.a)(t,e);var a=t.prototype;return a.getRef=function(e){this.props.innerRef&&this.props.innerRef(e),this.ref=e},a.focus=function(){this.ref&&this.ref.focus()},a.render=function(){var e=this.props,t=e.className,a=e.cssModule,o=e.type,r=e.bsSize,i=e.valid,l=e.invalid,d=e.tag,u=e.addon,b=e.plaintext,m=e.innerRef,h=Object(s.a)(e,["className","cssModule","type","bsSize","valid","invalid","tag","addon","plaintext","innerRef"]),g=["radio","checkbox"].indexOf(o)>-1,v=new RegExp("\\D","g"),O=d||("select"===o||"textarea"===o?o:"input"),j="form-control";b?(j+="-plaintext",O=d||"input"):"file"===o?j+="-file":g&&(j=u?null:"form-check-input"),h.size&&v.test(h.size)&&(Object(f.t)('Please use the prop "bsSize" instead of the "size" to bootstrap\'s input sizing.'),r=h.size,delete h.size);var N=Object(f.m)(p()(t,l&&"is-invalid",i&&"is-valid",!!r&&"form-control-"+r,j),a);return("input"===O||d&&"function"===typeof d)&&(h.type=o),h.children&&!b&&"select"!==o&&"string"===typeof O&&"select"!==O&&(Object(f.t)('Input with a type of "'+o+'" cannot have children. Please use "value"/"defaultValue" instead.'),delete h.children),c.a.createElement(O,Object(n.a)({},h,{ref:m,className:N}))},t}(c.a.Component);m.propTypes=b,m.defaultProps={type:"text"},t.a=m},594:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(566),r=a(35),i=a(1),c=a.n(i),l=a(6),d=a.n(l),u=a(84),p=a.n(u),f=a(590),b=a(574),m=a(40),h=a(575),g={caret:d.a.bool,color:d.a.string,children:d.a.node,className:d.a.string,cssModule:d.a.object,disabled:d.a.bool,onClick:d.a.func,"aria-haspopup":d.a.bool,split:d.a.bool,tag:m.q,nav:d.a.bool},v=function(e){function t(t){var a;return(a=e.call(this,t)||this).onClick=a.onClick.bind(Object(o.a)(a)),a}Object(r.a)(t,e);var a=t.prototype;return a.onClick=function(e){this.props.disabled||this.context.disabled?e.preventDefault():(this.props.nav&&!this.props.tag&&e.preventDefault(),this.props.onClick&&this.props.onClick(e),this.context.toggle(e))},a.render=function(){var e,t=this,a=this.props,o=a.className,r=a.color,i=a.cssModule,l=a.caret,d=a.split,u=a.nav,b=a.tag,g=a.innerRef,v=Object(s.a)(a,["className","color","cssModule","caret","split","nav","tag","innerRef"]),O=v["aria-label"]||"Toggle Dropdown",j=Object(m.m)(p()(o,{"dropdown-toggle":l||d,"dropdown-toggle-split":d,"nav-link":u}),i),N=v.children||c.a.createElement("span",{className:"sr-only"},O);return u&&!b?(e="a",v.href="#"):b?e=b:(e=h.a,v.color=r,v.cssModule=i),this.context.inNavbar?c.a.createElement(e,Object(n.a)({},v,{className:j,onClick:this.onClick,"aria-expanded":this.context.isOpen,children:N})):c.a.createElement(f.a,{innerRef:g},(function(a){var s,o=a.ref;return c.a.createElement(e,Object(n.a)({},v,((s={})["string"===typeof e?"ref":"innerRef"]=o,s),{className:j,onClick:t.onClick,"aria-expanded":t.context.isOpen,children:N}))}))},t}(c.a.Component);v.propTypes=g,v.defaultProps={"aria-haspopup":!0,color:"secondary"},v.contextType=b.a,t.a=v},595:function(e,t,a){"use strict";var n=a(21),s=a(74),o=a(45),r=a(35),i=a(1),c=a.n(i),l=a(6),d=a.n(l),u=a(84),p=a.n(u),f=a(666),b=a(574),m=a(40),h={tag:m.q,children:d.a.node.isRequired,right:d.a.bool,flip:d.a.bool,modifiers:d.a.object,className:d.a.string,cssModule:d.a.object,persist:d.a.bool,positionFixed:d.a.bool},g={flip:{enabled:!1}},v={up:"top",left:"left",right:"right",down:"bottom"},O=function(e){function t(){return e.apply(this,arguments)||this}return Object(r.a)(t,e),t.prototype.render=function(){var e=this,t=this.props,a=t.className,r=t.cssModule,i=t.right,l=t.tag,d=t.flip,u=t.modifiers,b=t.persist,h=t.positionFixed,O=Object(o.a)(t,["className","cssModule","right","tag","flip","modifiers","persist","positionFixed"]),j=Object(m.m)(p()(a,"dropdown-menu",{"dropdown-menu-right":i,show:this.context.isOpen}),r),N=l;if(b||this.context.isOpen&&!this.context.inNavbar){var y=(v[this.context.direction]||"bottom")+"-"+(i?"end":"start"),x=d?u:Object(s.a)({},u,{},g),E=!!h;return c.a.createElement(f.a,{placement:y,modifiers:x,positionFixed:E},(function(t){var a=t.ref,s=t.style,o=t.placement;return c.a.createElement(N,Object(n.a)({tabIndex:"-1",role:"menu",ref:a,style:s},O,{"aria-hidden":!e.context.isOpen,className:j,"x-placement":o}))}))}return c.a.createElement(N,Object(n.a)({tabIndex:"-1",role:"menu"},O,{"aria-hidden":!this.context.isOpen,className:j,"x-placement":O.placement}))},t}(c.a.Component);O.propTypes=h,O.defaultProps={tag:"div",flip:!0},O.contextType=b.a,t.a=O},596:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(566),r=a(35),i=a(1),c=a.n(i),l=a(6),d=a.n(l),u=a(84),p=a.n(u),f=a(574),b=a(40),m={children:d.a.node,active:d.a.bool,disabled:d.a.bool,divider:d.a.bool,tag:b.q,header:d.a.bool,onClick:d.a.func,className:d.a.string,cssModule:d.a.object,toggle:d.a.bool},h=function(e){function t(t){var a;return(a=e.call(this,t)||this).onClick=a.onClick.bind(Object(o.a)(a)),a.getTabIndex=a.getTabIndex.bind(Object(o.a)(a)),a}Object(r.a)(t,e);var a=t.prototype;return a.onClick=function(e){this.props.disabled||this.props.header||this.props.divider?e.preventDefault():(this.props.onClick&&this.props.onClick(e),this.props.toggle&&this.context.toggle(e))},a.getTabIndex=function(){return this.props.disabled||this.props.header||this.props.divider?"-1":"0"},a.render=function(){var e=this.getTabIndex(),t=e>-1?"menuitem":void 0,a=Object(b.n)(this.props,["toggle"]),o=a.className,r=a.cssModule,i=a.divider,l=a.tag,d=a.header,u=a.active,f=Object(s.a)(a,["className","cssModule","divider","tag","header","active"]),m=Object(b.m)(p()(o,{disabled:f.disabled,"dropdown-item":!i&&!d,active:u,"dropdown-header":d,"dropdown-divider":i}),r);return"button"===l&&(d?l="h6":i?l="div":f.href&&(l="a")),c.a.createElement(l,Object(n.a)({type:"button"===l&&(f.onClick||this.props.toggle)?"button":void 0},f,{tabIndex:e,role:t,className:m,onClick:this.onClick}))},t}(c.a.Component);h.propTypes=m,h.defaultProps={tag:"button",toggle:!0},h.contextType=f.a,t.a=h},605:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(566),r=a(35),i=a(1),c=a.n(i),l=a(6),d=a.n(l),u=a(84),p=a.n(u),f=a(40),b={children:d.a.node,inline:d.a.bool,tag:f.q,innerRef:d.a.oneOfType([d.a.object,d.a.func,d.a.string]),className:d.a.string,cssModule:d.a.object},m=function(e){function t(t){var a;return(a=e.call(this,t)||this).getRef=a.getRef.bind(Object(o.a)(a)),a.submit=a.submit.bind(Object(o.a)(a)),a}Object(r.a)(t,e);var a=t.prototype;return a.getRef=function(e){this.props.innerRef&&this.props.innerRef(e),this.ref=e},a.submit=function(){this.ref&&this.ref.submit()},a.render=function(){var e=this.props,t=e.className,a=e.cssModule,o=e.inline,r=e.tag,i=e.innerRef,l=Object(s.a)(e,["className","cssModule","inline","tag","innerRef"]),d=Object(f.m)(p()(t,!!o&&"form-inline"),a);return c.a.createElement(r,Object(n.a)({},l,{ref:i,className:d}))},t}(i.Component);m.propTypes=b,m.defaultProps={tag:"form"},t.a=m},610:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={tag:u.q,className:c.a.string,cssModule:c.a.object},f=function(e){var t=e.className,a=e.cssModule,o=e.tag,i=Object(s.a)(e,["className","cssModule","tag"]),c=Object(u.m)(d()(t,"card-footer"),a);return r.a.createElement(o,Object(n.a)({},i,{className:c}))};f.propTypes=p,f.defaultProps={tag:"div"},t.a=f},611:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={children:c.a.node,row:c.a.bool,check:c.a.bool,inline:c.a.bool,disabled:c.a.bool,tag:u.q,className:c.a.string,cssModule:c.a.object},f=function(e){var t=e.className,a=e.cssModule,o=e.row,i=e.disabled,c=e.check,l=e.inline,p=e.tag,f=Object(s.a)(e,["className","cssModule","row","disabled","check","inline","tag"]),b=Object(u.m)(d()(t,!!o&&"row",c?"form-check":"form-group",!(!c||!l)&&"form-check-inline",!(!c||!i)&&"disabled"),a);return"fieldset"===p&&(f.disabled=i),r.a.createElement(p,Object(n.a)({},f,{className:b}))};f.propTypes=p,f.defaultProps={tag:"div"},t.a=f},612:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p=c.a.oneOfType([c.a.number,c.a.string]),f=c.a.oneOfType([c.a.string,c.a.number,c.a.shape({size:p,order:p,offset:p})]),b={children:c.a.node,hidden:c.a.bool,check:c.a.bool,size:c.a.string,for:c.a.string,tag:u.q,className:c.a.string,cssModule:c.a.object,xs:f,sm:f,md:f,lg:f,xl:f,widths:c.a.array},m={tag:"label",widths:["xs","sm","md","lg","xl"]},h=function(e,t,a){return!0===a||""===a?e?"col":"col-"+t:"auto"===a?e?"col-auto":"col-"+t+"-auto":e?"col-"+a:"col-"+t+"-"+a},g=function(e){var t=e.className,a=e.cssModule,o=e.hidden,i=e.widths,c=e.tag,l=e.check,p=e.size,f=e.for,b=Object(s.a)(e,["className","cssModule","hidden","widths","tag","check","size","for"]),m=[];i.forEach((function(t,n){var s=e[t];if(delete b[t],s||""===s){var o,r=!n;if(Object(u.k)(s)){var i,c=r?"-":"-"+t+"-";o=h(r,t,s.size),m.push(Object(u.m)(d()(((i={})[o]=s.size||""===s.size,i["order"+c+s.order]=s.order||0===s.order,i["offset"+c+s.offset]=s.offset||0===s.offset,i))),a)}else o=h(r,t,s),m.push(o)}}));var g=Object(u.m)(d()(t,!!o&&"sr-only",!!l&&"form-check-label",!!p&&"col-form-label-"+p,m,!!m.length&&"col-form-label"),a);return r.a.createElement(c,Object(n.a)({htmlFor:f},b,{className:g}))};g.propTypes=b,g.defaultProps=m,t.a=g},629:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={tag:u.q,size:c.a.string,className:c.a.string,cssModule:c.a.object},f=function(e){var t=e.className,a=e.cssModule,o=e.tag,i=e.size,c=Object(s.a)(e,["className","cssModule","tag","size"]),l=Object(u.m)(d()(t,"input-group",i?"input-group-"+i:null),a);return r.a.createElement(o,Object(n.a)({},c,{className:l}))};f.propTypes=p,f.defaultProps={tag:"div"},t.a=f},630:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p=a(588),f={tag:u.q,addonType:c.a.oneOf(["prepend","append"]).isRequired,children:c.a.node,className:c.a.string,cssModule:c.a.object},b=function(e){var t=e.className,a=e.cssModule,o=e.tag,i=e.addonType,c=e.children,l=Object(s.a)(e,["className","cssModule","tag","addonType","children"]),f=Object(u.m)(d()(t,"input-group-"+i),a);return"string"===typeof c?r.a.createElement(o,Object(n.a)({},l,{className:f}),r.a.createElement(p.a,{children:c})):r.a.createElement(o,Object(n.a)({},l,{className:f,children:c}))};b.propTypes=f,b.defaultProps={tag:"div"},t.a=b},643:function(e,t,a){"use strict";var n,s=a(21),o=a(45),r=a(566),i=a(35),c=a(74),l=a(1),d=a.n(l),u=a(6),p=a.n(u),f=a(84),b=a.n(f),m=a(112),h=a(40),g=Object(c.a)({},m.Transition.propTypes,{isOpen:p.a.bool,children:p.a.oneOfType([p.a.arrayOf(p.a.node),p.a.node]),tag:h.q,className:p.a.node,navbar:p.a.bool,cssModule:p.a.object,innerRef:p.a.oneOfType([p.a.func,p.a.string,p.a.object])}),v=Object(c.a)({},m.Transition.defaultProps,{isOpen:!1,appear:!1,enter:!0,exit:!0,tag:"div",timeout:h.e.Collapse}),O=((n={})[h.d.ENTERING]="collapsing",n[h.d.ENTERED]="collapse show",n[h.d.EXITING]="collapsing",n[h.d.EXITED]="collapse",n);function j(e){return e.scrollHeight}var N=function(e){function t(t){var a;return(a=e.call(this,t)||this).state={height:null},["onEntering","onEntered","onExit","onExiting","onExited"].forEach((function(e){a[e]=a[e].bind(Object(r.a)(a))})),a}Object(i.a)(t,e);var a=t.prototype;return a.onEntering=function(e,t){this.setState({height:j(e)}),this.props.onEntering(e,t)},a.onEntered=function(e,t){this.setState({height:null}),this.props.onEntered(e,t)},a.onExit=function(e){this.setState({height:j(e)}),this.props.onExit(e)},a.onExiting=function(e){e.offsetHeight;this.setState({height:0}),this.props.onExiting(e)},a.onExited=function(e){this.setState({height:null}),this.props.onExited(e)},a.render=function(){var e=this,t=this.props,a=t.tag,n=t.isOpen,r=t.className,i=t.navbar,l=t.cssModule,u=t.children,p=(t.innerRef,Object(o.a)(t,["tag","isOpen","className","navbar","cssModule","children","innerRef"])),f=this.state.height,g=Object(h.o)(p,h.c),v=Object(h.n)(p,h.c);return d.a.createElement(m.Transition,Object(s.a)({},g,{in:n,onEntering:this.onEntering,onEntered:this.onEntered,onExit:this.onExit,onExiting:this.onExiting,onExited:this.onExited}),(function(t){var n=function(e){return O[e]||"collapse"}(t),o=Object(h.m)(b()(r,n,i&&"navbar-collapse"),l),p=null===f?null:{height:f};return d.a.createElement(a,Object(s.a)({},v,{style:Object(c.a)({},v.style,{},p),className:o,ref:e.props.innerRef}),u)}))},t}(l.Component);N.propTypes=g,N.defaultProps=v,t.a=N},900:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={children:c.a.node,inline:c.a.bool,tag:u.q,color:c.a.string,className:c.a.string,cssModule:c.a.object},f=function(e){var t=e.className,a=e.cssModule,o=e.inline,i=e.color,c=e.tag,l=Object(s.a)(e,["className","cssModule","inline","color","tag"]),p=Object(u.m)(d()(t,!o&&"form-text",!!i&&"text-"+i),a);return r.a.createElement(c,Object(n.a)({},l,{className:p}))};f.propTypes=p,f.defaultProps={tag:"small",color:"muted"},t.a=f},901:function(e,t,a){"use strict";var n=a(21),s=a(45),o=a(1),r=a.n(o),i=a(6),c=a.n(i),l=a(84),d=a.n(l),u=a(40),p={children:c.a.node,tag:u.q,className:c.a.string,cssModule:c.a.object,valid:c.a.bool,tooltip:c.a.bool},f={tag:"div",valid:void 0},b=function(e){var t=e.className,a=e.cssModule,o=e.valid,i=e.tooltip,c=e.tag,l=Object(s.a)(e,["className","cssModule","valid","tooltip","tag"]),p=i?"tooltip":"feedback",f=Object(u.m)(d()(t,o?"valid-"+p:"invalid-"+p),a);return r.a.createElement(c,Object(n.a)({},l,{className:f}))};b.propTypes=p,b.defaultProps=f,t.a=b},902:function(e,t,a){"use strict";var n=a(1),s=a.n(n),o=a(6),r=a.n(o),i=a(604),c={addonType:r.a.oneOf(["prepend","append"]).isRequired,children:r.a.node},l=function(e){return s.a.createElement(i.a,e)};l.propTypes=c,t.a=l}}]);
//# sourceMappingURL=13.6d29c4ac.chunk.js.map