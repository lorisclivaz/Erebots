(this["webpackJsonpcovid19-frontend"]=this["webpackJsonpcovid19-frontend"]||[]).push([[52],{568:function(e,a,t){"use strict";var r=t(21),n=t(45),s=t(1),c=t.n(s),l=t(6),o=t.n(l),u=t(84),m=t.n(u),i=t(40),d={tag:i.q,inverse:o.a.bool,color:o.a.string,body:o.a.bool,outline:o.a.bool,className:o.a.string,cssModule:o.a.object,innerRef:o.a.oneOfType([o.a.object,o.a.string,o.a.func])},f=function(e){var a=e.className,t=e.cssModule,s=e.color,l=e.body,o=e.inverse,u=e.outline,d=e.tag,f=e.innerRef,b=Object(n.a)(e,["className","cssModule","color","body","inverse","outline","tag","innerRef"]),g=Object(i.m)(m()(a,"card",!!o&&"text-white",!!l&&"card-body",!!s&&(u?"border":"bg")+"-"+s),t);return c.a.createElement(d,Object(r.a)({},b,{className:g,ref:f}))};f.propTypes=d,f.defaultProps={tag:"div"},a.a=f},569:function(e,a,t){"use strict";var r=t(21),n=t(45),s=t(1),c=t.n(s),l=t(6),o=t.n(l),u=t(84),m=t.n(u),i=t(40),d={tag:i.q,className:o.a.string,cssModule:o.a.object,innerRef:o.a.oneOfType([o.a.object,o.a.string,o.a.func])},f=function(e){var a=e.className,t=e.cssModule,s=e.innerRef,l=e.tag,o=Object(n.a)(e,["className","cssModule","innerRef","tag"]),u=Object(i.m)(m()(a,"card-body"),t);return c.a.createElement(l,Object(r.a)({},o,{className:u,ref:s}))};f.propTypes=d,f.defaultProps={tag:"div"},a.a=f},570:function(e,a,t){"use strict";var r=t(21),n=t(45),s=t(1),c=t.n(s),l=t(6),o=t.n(l),u=t(84),m=t.n(u),i=t(40),d=o.a.oneOfType([o.a.number,o.a.string]),f={tag:i.q,noGutters:o.a.bool,className:o.a.string,cssModule:o.a.object,form:o.a.bool,xs:d,sm:d,md:d,lg:d,xl:d},b={tag:"div",widths:["xs","sm","md","lg","xl"]},g=function(e){var a=e.className,t=e.cssModule,s=e.noGutters,l=e.tag,o=e.form,u=e.widths,d=Object(n.a)(e,["className","cssModule","noGutters","tag","form","widths"]),f=[];u.forEach((function(a,t){var r=e[a];if(delete d[a],r){var n=!t;f.push(n?"row-cols-"+r:"row-cols-"+a+"-"+r)}}));var b=Object(i.m)(m()(a,s?"no-gutters":null,o?"form-row":"row",f),t);return c.a.createElement(l,Object(r.a)({},d,{className:b}))};g.propTypes=f,g.defaultProps=b,a.a=g},571:function(e,a,t){"use strict";var r=t(21),n=t(45),s=t(1),c=t.n(s),l=t(6),o=t.n(l),u=t(84),m=t.n(u),i=t(40),d=o.a.oneOfType([o.a.number,o.a.string]),f=o.a.oneOfType([o.a.bool,o.a.number,o.a.string,o.a.shape({size:o.a.oneOfType([o.a.bool,o.a.number,o.a.string]),order:d,offset:d})]),b={tag:i.q,xs:f,sm:f,md:f,lg:f,xl:f,className:o.a.string,cssModule:o.a.object,widths:o.a.array},g={tag:"div",widths:["xs","sm","md","lg","xl"]},p=function(e,a,t){return!0===t||""===t?e?"col":"col-"+a:"auto"===t?e?"col-auto":"col-"+a+"-auto":e?"col-"+t:"col-"+a+"-"+t},v=function(e){var a=e.className,t=e.cssModule,s=e.widths,l=e.tag,o=Object(n.a)(e,["className","cssModule","widths","tag"]),u=[];s.forEach((function(a,r){var n=e[a];if(delete o[a],n||""===n){var s=!r;if(Object(i.k)(n)){var c,l=s?"-":"-"+a+"-",d=p(s,a,n.size);u.push(Object(i.m)(m()(((c={})[d]=n.size||""===n.size,c["order"+l+n.order]=n.order||0===n.order,c["offset"+l+n.offset]=n.offset||0===n.offset,c)),t))}else{var f=p(s,a,n);u.push(f)}}})),u.length||u.push("col");var d=Object(i.m)(m()(a,u),t);return c.a.createElement(l,Object(r.a)({},o,{className:d}))};v.propTypes=b,v.defaultProps=g,a.a=v},572:function(e,a,t){"use strict";var r=t(21),n=t(45),s=t(1),c=t.n(s),l=t(6),o=t.n(l),u=t(84),m=t.n(u),i=t(40),d={tag:i.q,className:o.a.string,cssModule:o.a.object},f=function(e){var a=e.className,t=e.cssModule,s=e.tag,l=Object(n.a)(e,["className","cssModule","tag"]),o=Object(i.m)(m()(a,"card-header"),t);return c.a.createElement(s,Object(r.a)({},l,{className:o}))};f.propTypes=d,f.defaultProps={tag:"div"},a.a=f},895:function(e,a,t){"use strict";t.r(a);var r=t(72),n=t(73),s=t(195),c=t(194),l=t(1),o=t.n(l),u=t(570),m=t(571),i=t(568),d=t(572),f=t(569),b=t(886),g=t(885),p=function(e){Object(s.a)(t,e);var a=Object(c.a)(t);function t(){return Object(r.a)(this,t),a.apply(this,arguments)}return Object(n.a)(t,[{key:"render",value:function(){return o.a.createElement("div",{className:"animated fadeIn"},o.a.createElement(u.a,null,o.a.createElement(m.a,{xs:"12"},o.a.createElement(i.a,null,o.a.createElement(d.a,null,o.a.createElement("i",{className:"fa fa-align-justify"}),o.a.createElement("strong",null,"Breadcrumbs"),o.a.createElement("div",{className:"card-header-actions"},o.a.createElement("a",{href:"https://reactstrap.github.io/components/breadcrumbs/",rel:"noreferrer noopener",target:"_blank",className:"card-header-action"},o.a.createElement("small",{className:"text-muted"},"docs")))),o.a.createElement(f.a,null,o.a.createElement(b.a,null,o.a.createElement(g.a,{active:!0},"Home")),o.a.createElement(b.a,null,o.a.createElement(g.a,null,o.a.createElement("a",{href:"#"},"Home")),o.a.createElement(g.a,{active:!0},"Library")),o.a.createElement(b.a,null,o.a.createElement(g.a,null,o.a.createElement("a",{href:"#"},"Home")),o.a.createElement(g.a,null,o.a.createElement("a",{href:"#"},"Library")),o.a.createElement(g.a,{active:!0},"Data")),o.a.createElement(b.a,{tag:"nav"},o.a.createElement(g.a,{tag:"a",href:"#"},"Home"),o.a.createElement(g.a,{tag:"a",href:"#"},"Library"),o.a.createElement(g.a,{tag:"a",href:"#"},"Data"),o.a.createElement(g.a,{active:!0,tag:"span"},"Bootstrap")))))))}}]),t}(l.Component);a.default=p}}]);
//# sourceMappingURL=52.361b2d95.chunk.js.map