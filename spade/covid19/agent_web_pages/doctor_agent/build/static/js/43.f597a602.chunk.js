(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[43],{568:function(e,a,t){"use strict";var n=t(21),r=t(45),l=t(1),c=t.n(l),o=t(6),i=t.n(o),s=t(84),d=t.n(s),u=t(40),m={tag:u.q,inverse:i.a.bool,color:i.a.string,body:i.a.bool,outline:i.a.bool,className:i.a.string,cssModule:i.a.object,innerRef:i.a.oneOfType([i.a.object,i.a.string,i.a.func])},p=function(e){var a=e.className,t=e.cssModule,l=e.color,o=e.body,i=e.inverse,s=e.outline,m=e.tag,p=e.innerRef,f=Object(r.a)(e,["className","cssModule","color","body","inverse","outline","tag","innerRef"]),h=Object(u.m)(d()(a,"card",!!i&&"text-white",!!o&&"card-body",!!l&&(s?"border":"bg")+"-"+l),t);return c.a.createElement(m,Object(n.a)({},f,{className:h,ref:p}))};p.propTypes=m,p.defaultProps={tag:"div"},a.a=p},569:function(e,a,t){"use strict";var n=t(21),r=t(45),l=t(1),c=t.n(l),o=t(6),i=t.n(o),s=t(84),d=t.n(s),u=t(40),m={tag:u.q,className:i.a.string,cssModule:i.a.object,innerRef:i.a.oneOfType([i.a.object,i.a.string,i.a.func])},p=function(e){var a=e.className,t=e.cssModule,l=e.innerRef,o=e.tag,i=Object(r.a)(e,["className","cssModule","innerRef","tag"]),s=Object(u.m)(d()(a,"card-body"),t);return c.a.createElement(o,Object(n.a)({},i,{className:s,ref:l}))};p.propTypes=m,p.defaultProps={tag:"div"},a.a=p},572:function(e,a,t){"use strict";var n=t(21),r=t(45),l=t(1),c=t.n(l),o=t(6),i=t.n(o),s=t(84),d=t.n(s),u=t(40),m={tag:u.q,className:i.a.string,cssModule:i.a.object},p=function(e){var a=e.className,t=e.cssModule,l=e.tag,o=Object(r.a)(e,["className","cssModule","tag"]),i=Object(u.m)(d()(a,"card-header"),t);return c.a.createElement(l,Object(n.a)({},o,{className:i}))};p.propTypes=m,p.defaultProps={tag:"div"},a.a=p},590:function(e,a,t){"use strict";t.d(a,"a",(function(){return E}));var n=t(573),r=t.n(n),l=t(576),c=t.n(l),o=t(579),i=t.n(o),s=t(581),d=t.n(s),u=t(1),m=t(586),p=t.n(m),f=t(585),h=t(589),b=function(e){function a(){for(var a,t=arguments.length,n=new Array(t),r=0;r<t;r++)n[r]=arguments[r];return a=e.call.apply(e,[this].concat(n))||this,d()(c()(a),"refHandler",(function(e){Object(h.b)(a.props.innerRef,e),Object(h.a)(a.props.setReferenceNode,e)})),a}i()(a,e);var t=a.prototype;return t.componentWillUnmount=function(){Object(h.b)(this.props.innerRef,null)},t.render=function(){return p()(Boolean(this.props.setReferenceNode),"`Reference` should not be used outside of a `Manager` component."),Object(h.c)(this.props.children)({ref:this.refHandler})},a}(u.Component);function E(e){return u.createElement(f.b.Consumer,null,(function(a){return u.createElement(b,r()({setReferenceNode:a},e))}))}},594:function(e,a,t){"use strict";var n=t(21),r=t(45),l=t(566),c=t(35),o=t(1),i=t.n(o),s=t(6),d=t.n(s),u=t(84),m=t.n(u),p=t(590),f=t(574),h=t(40),b=t(575),E={caret:d.a.bool,color:d.a.string,children:d.a.node,className:d.a.string,cssModule:d.a.object,disabled:d.a.bool,onClick:d.a.func,"aria-haspopup":d.a.bool,split:d.a.bool,tag:h.q,nav:d.a.bool},g=function(e){function a(a){var t;return(t=e.call(this,a)||this).onClick=t.onClick.bind(Object(l.a)(t)),t}Object(c.a)(a,e);var t=a.prototype;return t.onClick=function(e){this.props.disabled||this.context.disabled?e.preventDefault():(this.props.nav&&!this.props.tag&&e.preventDefault(),this.props.onClick&&this.props.onClick(e),this.context.toggle(e))},t.render=function(){var e,a=this,t=this.props,l=t.className,c=t.color,o=t.cssModule,s=t.caret,d=t.split,u=t.nav,f=t.tag,E=t.innerRef,g=Object(r.a)(t,["className","color","cssModule","caret","split","nav","tag","innerRef"]),v=g["aria-label"]||"Toggle Dropdown",O=Object(h.m)(m()(l,{"dropdown-toggle":s||d,"dropdown-toggle-split":d,"nav-link":u}),o),k=g.children||i.a.createElement("span",{className:"sr-only"},v);return u&&!f?(e="a",g.href="#"):f?e=f:(e=b.a,g.color=c,g.cssModule=o),this.context.inNavbar?i.a.createElement(e,Object(n.a)({},g,{className:O,onClick:this.onClick,"aria-expanded":this.context.isOpen,children:k})):i.a.createElement(p.a,{innerRef:E},(function(t){var r,l=t.ref;return i.a.createElement(e,Object(n.a)({},g,((r={})["string"===typeof e?"ref":"innerRef"]=l,r),{className:O,onClick:a.onClick,"aria-expanded":a.context.isOpen,children:k}))}))},a}(i.a.Component);g.propTypes=E,g.defaultProps={"aria-haspopup":!0,color:"secondary"},g.contextType=f.a,a.a=g},595:function(e,a,t){"use strict";var n=t(21),r=t(74),l=t(45),c=t(35),o=t(1),i=t.n(o),s=t(6),d=t.n(s),u=t(84),m=t.n(u),p=t(666),f=t(574),h=t(40),b={tag:h.q,children:d.a.node.isRequired,right:d.a.bool,flip:d.a.bool,modifiers:d.a.object,className:d.a.string,cssModule:d.a.object,persist:d.a.bool,positionFixed:d.a.bool},E={flip:{enabled:!1}},g={up:"top",left:"left",right:"right",down:"bottom"},v=function(e){function a(){return e.apply(this,arguments)||this}return Object(c.a)(a,e),a.prototype.render=function(){var e=this,a=this.props,t=a.className,c=a.cssModule,o=a.right,s=a.tag,d=a.flip,u=a.modifiers,f=a.persist,b=a.positionFixed,v=Object(l.a)(a,["className","cssModule","right","tag","flip","modifiers","persist","positionFixed"]),O=Object(h.m)(m()(t,"dropdown-menu",{"dropdown-menu-right":o,show:this.context.isOpen}),c),k=s;if(f||this.context.isOpen&&!this.context.inNavbar){var j=(g[this.context.direction]||"bottom")+"-"+(o?"end":"start"),N=d?u:Object(r.a)({},u,{},E),y=!!b;return i.a.createElement(p.a,{placement:j,modifiers:N,positionFixed:y},(function(a){var t=a.ref,r=a.style,l=a.placement;return i.a.createElement(k,Object(n.a)({tabIndex:"-1",role:"menu",ref:t,style:r},v,{"aria-hidden":!e.context.isOpen,className:O,"x-placement":l}))}))}return i.a.createElement(k,Object(n.a)({tabIndex:"-1",role:"menu"},v,{"aria-hidden":!this.context.isOpen,className:O,"x-placement":v.placement}))},a}(i.a.Component);v.propTypes=b,v.defaultProps={tag:"div",flip:!0},v.contextType=f.a,a.a=v},596:function(e,a,t){"use strict";var n=t(21),r=t(45),l=t(566),c=t(35),o=t(1),i=t.n(o),s=t(6),d=t.n(s),u=t(84),m=t.n(u),p=t(574),f=t(40),h={children:d.a.node,active:d.a.bool,disabled:d.a.bool,divider:d.a.bool,tag:f.q,header:d.a.bool,onClick:d.a.func,className:d.a.string,cssModule:d.a.object,toggle:d.a.bool},b=function(e){function a(a){var t;return(t=e.call(this,a)||this).onClick=t.onClick.bind(Object(l.a)(t)),t.getTabIndex=t.getTabIndex.bind(Object(l.a)(t)),t}Object(c.a)(a,e);var t=a.prototype;return t.onClick=function(e){this.props.disabled||this.props.header||this.props.divider?e.preventDefault():(this.props.onClick&&this.props.onClick(e),this.props.toggle&&this.context.toggle(e))},t.getTabIndex=function(){return this.props.disabled||this.props.header||this.props.divider?"-1":"0"},t.render=function(){var e=this.getTabIndex(),a=e>-1?"menuitem":void 0,t=Object(f.n)(this.props,["toggle"]),l=t.className,c=t.cssModule,o=t.divider,s=t.tag,d=t.header,u=t.active,p=Object(r.a)(t,["className","cssModule","divider","tag","header","active"]),h=Object(f.m)(m()(l,{disabled:p.disabled,"dropdown-item":!o&&!d,active:u,"dropdown-header":d,"dropdown-divider":o}),c);return"button"===s&&(d?s="h6":o?s="div":p.href&&(s="a")),i.a.createElement(s,Object(n.a)({type:"button"===s&&(p.onClick||this.props.toggle)?"button":void 0},p,{tabIndex:e,role:a,className:h,onClick:this.onClick}))},a}(i.a.Component);b.propTypes=h,b.defaultProps={tag:"button",toggle:!0},b.contextType=p.a,a.a=b},903:function(e,a,t){"use strict";t.r(a);var n=t(72),r=t(73),l=t(108),c=t(195),o=t(194),i=t(1),s=t.n(i),d=t(568),u=t(572),m=t(569),p=t(660),f=t(887),h=t(888),b=t(604),E=t(594),g=t(595),v=t(596),O=function(e){Object(c.a)(t,e);var a=Object(o.a)(t);function t(e){var r;return Object(n.a)(this,t),(r=a.call(this,e)).toggle=r.toggle.bind(Object(l.a)(r)),r.state={dropdownOpen:[!1,!1]},r}return Object(r.a)(t,[{key:"toggle",value:function(e){var a=this.state.dropdownOpen.map((function(a,t){return t===e&&!a}));this.setState({dropdownOpen:a})}},{key:"render",value:function(){var e=this;return s.a.createElement("div",{className:"animated fadeIn"},s.a.createElement(d.a,null,s.a.createElement(u.a,null,s.a.createElement("i",{className:"fa fa-align-justify"}),s.a.createElement("strong",null,"Navs"),s.a.createElement("div",{className:"card-header-actions"},s.a.createElement("a",{href:"https://reactstrap.github.io/components/navs/",rel:"noreferrer noopener",target:"_blank",className:"card-header-action"},s.a.createElement("small",{className:"text-muted"},"docs")))),s.a.createElement(m.a,null,s.a.createElement("p",null,"List Based"),s.a.createElement(p.a,null,s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Another Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{disabled:!0,href:"#"},"Disabled Link"))),s.a.createElement("hr",null),s.a.createElement("p",null,"Link Based"),s.a.createElement(p.a,null,s.a.createElement(h.a,{href:"#"},"Link")," ",s.a.createElement(h.a,{href:"#"},"Link")," ",s.a.createElement(h.a,{href:"#"},"Another Link")," ",s.a.createElement(h.a,{disabled:!0,href:"#"},"Disabled Link")))),s.a.createElement(d.a,null,s.a.createElement(u.a,null,s.a.createElement("i",{className:"fa fa-align-justify"}),s.a.createElement("strong",null,"Navs Tabs")),s.a.createElement(m.a,null,s.a.createElement(p.a,{tabs:!0},s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#",active:!0},"Link")),s.a.createElement(b.a,{nav:!0,isOpen:this.state.dropdownOpen[0],toggle:function(){e.toggle(0)}},s.a.createElement(E.a,{nav:!0,caret:!0},"Dropdown"),s.a.createElement(g.a,null,s.a.createElement(v.a,{header:!0},"Header"),s.a.createElement(v.a,{disabled:!0},"Action"),s.a.createElement(v.a,null,"Another Action"),s.a.createElement(v.a,{divider:!0}),s.a.createElement(v.a,null,"Another Action"))),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Another Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{disabled:!0,href:"#"},"Disabled Link"))))),s.a.createElement(d.a,null,s.a.createElement(u.a,null,s.a.createElement("i",{className:"fa fa-align-justify"}),s.a.createElement("strong",null,"Navs Pills")),s.a.createElement(m.a,null,s.a.createElement(p.a,{pills:!0},s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#",active:!0},"Link")),s.a.createElement(b.a,{nav:!0,isOpen:this.state.dropdownOpen[1],toggle:function(){e.toggle(1)}},s.a.createElement(E.a,{nav:!0,caret:!0},"Dropdown"),s.a.createElement(g.a,null,s.a.createElement(v.a,{header:!0},"Header"),s.a.createElement(v.a,{disabled:!0},"Action"),s.a.createElement(v.a,null,"Another Action"),s.a.createElement(v.a,{divider:!0}),s.a.createElement(v.a,null,"Another Action"))),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Another Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{disabled:!0,href:"#"},"Disabled Link"))))),s.a.createElement(d.a,null,s.a.createElement(u.a,null,s.a.createElement("i",{className:"fa fa-align-justify"}),s.a.createElement("strong",null,"Navs Vertical")),s.a.createElement(m.a,null,s.a.createElement("p",null,"List Based"),s.a.createElement(p.a,{vertical:!0},s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{href:"#"},"Another Link")),s.a.createElement(f.a,null,s.a.createElement(h.a,{disabled:!0,href:"#"},"Disabled Link"))),s.a.createElement("hr",null),s.a.createElement("p",null,"Link based"),s.a.createElement(p.a,{vertical:!0},s.a.createElement(h.a,{href:"#"},"Link")," ",s.a.createElement(h.a,{href:"#"},"Link")," ",s.a.createElement(h.a,{href:"#"},"Another Link")," ",s.a.createElement(h.a,{disabled:!0,href:"#"},"Disabled Link")))))}}]),t}(i.Component);a.default=O}}]);
//# sourceMappingURL=43.f597a602.chunk.js.map