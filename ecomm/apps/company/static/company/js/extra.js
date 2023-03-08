function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const currentCompanyAlias = () => {
    return `/${document.querySelector('html').dataset.company}`;
}

const currentLocation = (expr='hostname') => {
    let location = null
    switch (expr) {
        case 'hostname':
            location = window.location.hostname
            break;
        case 'pathname':
            location = window.location.pathname
            break;
        case 'protocol':
            location = window.location.protocol
            break;
        case 'assign':
            location = window.location.assign()
            break;
        case 'base':
            location = window.location.href.split('?')[0]
            break;
        case 'params':
            location = window.location.href.split('?')[1]
            break;
        case 'search':
            location = window.location.search
            break;
        default:
            location = window.location.href
    }
    return location
}

class Logger {
    constructor(options) {
        this.infoMsgPrefix = options.infPref;
        this.errorMsgPrefix = options.errPref;
        this.off = options.off;
    }
    info(msg='') {
        if (!this.off) {
            console.log(`${this.infoMsgPrefix}: ${this.name}: ${msg}`);
        }
    }
    error(msg='') {
        if (!this.off) {
            console.log(`${this.errorMsgPrefix}: ${this.name}: ${msg}`);
        }
    }
}

const logger = new Logger({
    infPref: 'INFO',
    errPref: 'ERROR',
    off: false,
})

const isExist = (obj) => {
    return (obj != null && obj !== undefined || (Array.isArray(obj) && obj.length != 0))
}

const parseIntOrZero = (val) => {
    const parsed = parseInt(val);
    return (isNaN(parsed))? 0 : parsed; 
}

const inputDefault = (defVal) => {
    return function() {
        event.target.value = (event.target.value.length == 0)? defVal : event.target.value;
    };
};
const inputDefaultOne = inputDefault(1);

const onlyOneToNine = (evt) => {
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 49 || ASCIICode > 57)) {
        return false;
    }
    return true;
} // <input type="text" onkeypress="return onlyOneToNine(event);">

const onlyZeroToNine = (evt) => {
    var ASCIICode = (evt.which) ? evt.which : evt.keyCode
    if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57)) {
        return false;
    }
    return true;
} // <input type="text" onkeypress="return onlyOneToNine(event);">

const getBySelector = (selector, single=true) => {
    let res = null;
    if (single) {
        try {
            res = document.querySelector(selector);
        } catch(e) {
            if (e instanceof SyntaxError) {
                logger.info.call(this, `selector syntax ${selector}`);
            } else {
                logger.info.call(this, `querySelector by:${selector}`);
            }
        }
        if (res == null) {
            logger.info.call(this, `element(s) with selector ${selector} undefined`); 
        }
        return res;
    } else {
        try {
            res = document.querySelectorAll(selector);
        } catch(e) {
            if (e instanceof SyntaxError) {
                logger.info.call(this, `selector syntax ${selector}`);
            } else {
                logger.info.call(this, `querySelectorAll by:${selector}`);
            }
        }
        if (res.length == 0) {
            logger.info.call(this, `element(s) with selector ${selector} undefined`);
            return [];
        }
        return [...res];
    }
}

const getInnerHtml = (selector) => {
    let res = getBySelector(selector);
    if (isExist(res)) { 
        return res.innerHTML;
    }
}
const setInnerHtml = (selector, innerData) => {
    let res = getBySelector(selector);
    if (isExist(res)) { 
        res.innerHTML = innerData;
    }
}

Array.prototype.findElementIndex = function(el) {
    const index = this.indexOf(el);
    return (index != -1) ? index : null;
}


Element.prototype.hiddenParentByСondition = function(condition) {
    if (condition) {
        if (this.parentElement.classList.contains('hidden')) {
            this.parentElement.classList.remove('hidden');
        }
    } else {
        if (!this.parentElement.classList.contains('hidden')) {
            this.parentElement.classList.add('hidden');
        }
    }
}

class FetchDataException extends Error {
    constructor(message, options=null) {
        super(message, options);
    }
}

async function fetchAsync(method, url, data) {
    const requestOptions = {
        method: method,
        headers: { 
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify(data),
    };
    try {
        const response = await fetch(url, requestOptions);
        const res = await response.json();
        return res;
    } catch (e) {
        throw new FetchDataException(`ERROR: fetch data by URL: ${url}: ${e}`);
    }
}

class CssClassManager {
    
    add(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(!el.classList.contains(className)) {
                        el.classList.add(className)
                    }
                })
            } else {
                if(!res.classList.contains(className)) {
                    res.classList.add(className)
                }
            }
        }
    }
    remove(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(el.classList.contains(className)) {
                        el.classList.remove(className)
                    }
                })
            } else {
                if(res.classList.contains(className)) {
                    res.classList.remove(className)
                }
            }
        }
    }
    toggle(selector, className, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    el.classList.toggle(className)
                })
            } else {
                res.classList.toggle(className)
            }
        }
    }
    changeOrAddAt(selector, from, to, single=true) {
        let res = getBySelector(selector, single);
        if (isExist(res)) { 
            if (Array.isArray(res)) {
                res.forEach(el => {
                    if(!el.classList.contains(from)) {
                        el.classList.add(from)
                    } else {
                        el.classList.toggle(from)
                        el.classList.toggle(to)
                    }
                })
            } else {
                if(!res.classList.contains(from)) {
                    res.classList.add(from)
                } else {
                    res.classList.toggle(from)
                    res.classList.toggle(to)
                }
            }
        }
        
    }
    changeByPref(classes, single=true) {
        /* Change each class that start with prefix(until '-'), remove old valua and add new */
        classes.split(' ').forEach(className => {
            const namePref = className.split('-')[0];
            let res = getBySelector(`[class*="${namePref}"]`, single);
            if (isExist(res)) { 
                if (Array.isArray(res)) {
                    res.forEach(el => {
                        el.classList.forEach(name => {
                            if(name.startsWith(namePref) && name != className) { 
                                el.classList.toggle(name)
                                el.classList.toggle(className)
                            }
                        })
                    })
                } else {
                    res.classList.forEach(name => {
                        if(name.startsWith(namePref) && name != className) {
                            res.classList.toggle(name)
                            res.classList.toggle(className)
                        }
                    })
                }
            }
            
        })
    }
}

const cssClass = new CssClassManager()

class CartMamager {
    constructor(options) {
        this.addUrl = currentCompanyAlias()+options.addUrl;
        this.updateUrl = currentCompanyAlias()+options.updateUrl;
        this.deleteUrl = currentCompanyAlias()+options.deleteUrl;
        this.deliveryUpdateUrl = options.deliveryUpdateUrl;
        this.cartCountSelector = document.querySelector(options.cartCountSelector);
        this.cartTotalSelector = document.querySelector(options.cartTotalSelector);
        this.cartSubtotalSelector = document.querySelector(options.cartSubtotalSelector);
        this.boxElem = document.querySelector(options.boxSelector);
        this.boxCountElem = document.querySelector(options.boxCountSelector);
        this.boxCount = parseIntOrZero(getInnerHtml(options.boxCountSelector));
        this.deliveryElem = document.querySelector(options.deliverySelector);
        this.cartBoxElem = document.querySelector(options.cartBoxSelector);
        this.quantityKeySelector = options.quantityKeySelector;
        this.totalPriceProdKeySelector = options.totalPriceProdKeySelector;
        this.prodKeySelector = options.prodKeySelector;
        this.boxes = [];
        this.setup();
    }
    setup() {
        if (isExist(this.boxElem)) {
            this.boxElem.addEventListener('animationend', (ev) => {
                if (ev.animationName == 'box_scale') {
                    this.boxElem.classList.remove('box_scale');
                }
            });
        }
    }
    getProdId(el) {
        if (el.hasAttribute('data-prodid') && (parseIntOrZero(el.dataset.prodid) != 0)) {
            return el.dataset.prodid;
        }
        return null;
    }
    getProdCounter(el) {
        let prodId = this.getProdId(el);
        return document.querySelector(`#${this.quantityKeySelector}${prodId}`);
    }
    setPordQuantity(el, qty) {
        el.dataset.quantity = qty;
    }
    getPordQuantity(el) {
        return parseIntOrZero(el.dataset.quantity);
    }
    setProductBtnBgColor(el) {
        let qty = this.getPordQuantity(el);
        if (qty > 0) {
            el.classList.remove('btn-primary');
            el.classList.add('btn-success');

            el.querySelector('span:nth-child(1)').classList.toggle('hidden');
            el.querySelector('span:nth-child(2)').classList.toggle('hidden');
        }
    }
    setBoxTotalCount(res) {
        let count = res['quantity'];
        this.boxCountElem.innerHTML = (count==0)? '' : count;
        this.boxCountElem.hiddenParentByСondition(count > 0);
    }
    setCartQuantity(res) {
        let qty = res['quantity'];
        this.cartCountSelector.innerHTML = (qty==0)? '0' : qty;
    }
    setCartTotal(res) {
        let price = res['total_price'];
        this.cartTotalSelector.innerHTML = (price==0)? '0' : price;
    }
    setCartSubtotal(res) {
        let price = res['subtotal_price'];
        this.cartSubtotalSelector.innerHTML = (price==0)? '0' : price;
    }
    setCartProdTotal(res) {
        if (isExist(this.totalPriceProdKeySelector)) {
            let prod_total_price = res['prod_total_price'];
            let prodId = res['id'];
            let prodTotal = document.querySelector(`#${this.totalPriceProdKeySelector}${prodId}`);
            prodTotal.innerHTML = (prod_total_price==0)? '0' : prod_total_price;
        }
    }
    setProdCount(el, res) {
        if (el.tagName.toLowerCase() === 'input') {
            el.value = res['prod_quantity'];
        }
        if (el.tagName.toLowerCase() === 'span') {
            el.innerHTML = res['prod_quantity'];
        }
    }
    setBoxElemAnimation(res) {
        if (isExist(this.boxElem)) {
            let count = res['quantity'];
            if(count > 0) {
                if (!this.boxElem.classList.contains('text-success')) {
                    this.boxElem.classList.add('text-success');
                    this.boxElem.classList.add('box_scale');
                } else {
                    this.boxElem.classList.add('box_scale');
                }
            }
            if(count == 0 && this.boxElem.classList.contains('text-success')) {
                this.boxElem.classList.remove('text-success');
                this.boxElem.classList.add('box_scale');
            }
        }
    }
    setProdBtnCount(el) {
        let qty = this.getPordQuantity(el);
        let itemProdCountElem = el.querySelector('small');
        if (isExist(itemProdCountElem)) {
            itemProdCountElem.innerHTML = (qty==0)? '' : qty;
            itemProdCountElem.hiddenParentByСondition(qty > 0);
        }
    }
    hiddenCartBox(res) {
        if (res['quantity'] == 0) {
            this.cartBoxElem.classList.add('hidden');
            const emptyCartElem = document.querySelector(`#${this.cartBoxElem.id}-empty`);
            emptyCartElem.classList.remove('hidden');
        }
    }
    selectProduct(el, res) {
        this.setPordQuantity(el, 1);
        this.setProdBtnCount(el);
        this.setProductBtnBgColor(el);
        this.setBoxTotalCount(res);
        this.setBoxElemAnimation(res);
    }
    changeProdQuantityInCart(el, res) {
        this.setPordQuantity(el, res['prod_quantity']);
        this.setBoxTotalCount(res);
        this.setCartQuantity(res);
        this.setCartTotal(res);
        this.setCartSubtotal(res);
        this.setCartProdTotal(res);
        this.setBoxElemAnimation(res);
        // el.innerHTML = res['prod_quantity'];
        this.setProdCount(el, res);
        
    }
    
    deleteProdFromCart(res) {
        let prodId = res['id'];
        this.setBoxTotalCount(res);
        this.setCartQuantity(res);
        this.setCartTotal(res);
        this.setCartSubtotal(res);
        this.setBoxElemAnimation(res);
        let prodDel = document.querySelector(`#${this.prodKeySelector}${prodId}`);
        prodDel.remove();
        this.hiddenCartBox(res);
    }
    selectDelivery(res) {
        this.deliveryElem.innerHTML = res['delivery_price']
        this.setCartTotal(res);
    }
    select() {
        const el = event.target;
        let prodId = this.getProdId(el);
        let prodQty = this.getPordQuantity(el)
        if (prodId !== null) {
            if (prodQty == 0) {
                let prodQty = 1;
                this.add(el, prodId, prodQty);
            }
        }
    }
    increment() {
        const el = this.getProdCounter(event.target);
        let prodId = this.getProdId(el);
        let prodQty = this.getPordQuantity(el) + 1;
        if (prodId !== null) {
            this.update(el, prodId, prodQty);
        }
    }
    decrement() {
        const el = this.getProdCounter(event.target);
        let prodId = this.getProdId(el);
        let prodQty = this.getPordQuantity(el) - 1;
        if (prodId !== null && prodQty > 0) {
            this.update(el, prodId, prodQty);
        }
    }
    remove() {
        const el = event.target;
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.delete(el, prodId);
        }
    }
    addDelivery() {
        const el = event.target;
        let deliveryId = parseIntOrZero(el.value);
        // if (deliveryId !== 0) {
        this.delivery(el, deliveryId);
        // }
    }
    add(el, prodId, prodQty) {
        const data = {
            id: prodId,
            quantity: prodQty,
        }
        fetchAsync('POST', this.addUrl, data)
            .then(res => {
                this.selectProduct(el, res);
            })
    }
    update(el, prodId, prodQty) {
        const data = {
            id: prodId,
            quantity: prodQty,
        }
        fetchAsync('POST', this.updateUrl, data)
            .then(res => {
                this.changeProdQuantityInCart(el, res);
            })
    }
    delete(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.deleteUrl, data)
            .then(res => {
                this.deleteProdFromCart(res);
            })
    }
    delivery(el, deliveryId) {
        const data = {
            id: deliveryId,
        }
        fetchAsync('POST', this.deliveryUpdateUrl, data)
            .then(res => {
                this.selectDelivery(res);
            })
    }
}

const cart = new CartMamager({
    addUrl: '/shop/cart/add/',
    updateUrl: '/shop/cart/update/',
    deleteUrl: '/shop/cart/delete/',
    deliveryUpdateUrl: '/checkout/update-delivery/',
    boxSelector: '#cart-icon', // '#box-fix svg',
    boxCountSelector: '#cart-counter span',
    cartCountSelector: '#cart-quantity',
    cartTotalSelector: '#cart-total',
    cartSubtotalSelector: '#cart-subtotal',
    deliverySelector: '#cart-delivery',
    cartBoxSelector: '#cart-table',
    totalPriceProdKeySelector: 'prod-total-',
    quantityKeySelector: 'prod-quantity-',
    prodKeySelector: 'cart-prod-',
})

class WishMamager {
    constructor(options) {
        this.addUrl = currentCompanyAlias()+options.addUrl;
        this.deleteUrl = currentCompanyAlias()+options.deleteUrl;
        this.wishElem = document.querySelector(options.wishSelector);
        this.wishCountElem = document.querySelector(options.wishCountSelector);
        this.wishCount = parseIntOrZero(getInnerHtml(options.wishCountSelector));
        this.wishedClass = options.wishedClass;
        this.animationClass = options.animationClass;
        // this.wishes = [];
        this.setup();
    }
    setup() {
        if (isExist(this.wishElem) && isExist(this.animationClass)) {
            this.wishElem.addEventListener('animationend', (ev) => {
                if (ev.animationName == this.animationClas) {
                    this.wishElem.classList.remove(this.animationClass);
                }
            });
        }
    }
    getProdId(el) {
        if (el.hasAttribute('data-prodid') && (parseIntOrZero(el.dataset.prodid) != 0)) {
            return el.dataset.prodid;
        }
        return null;
    }
    setWishCount(count) {
        this.wishCountElem.innerHTML = (count == 0 )? '' : count;
        this.wishCountElem.hiddenParentByСondition(count > 0);
    } 
    setWishElemColor(count) {
        if(count > 0) {
            if (!this.wishElem.classList.contains(this.wishedClass)) {
                this.wishElem.classList.add(this.wishedClass);
                if (isExist(this.animationClass)) {
                    this.wishElem.classList.add(this.animationClas);
                }
            } else {
                if (isExist(this.animationClass)) {
                    this.wishElem.classList.add(this.animationClas);
                }
            }
        }
        if(count == 0 && this.wishElem.classList.contains(this.wishedClass)) {
            this.wishElem.classList.remove(this.wishedClass);
            if (isExist(this.animationClass)) {
                this.wishElem.classList.add(this.animationClass);
            }
        }
    }
    selectProduct(el, res) {
        let itemIconElem = el.querySelector('i');
        itemIconElem.classList.add(this.wishedClass);
        this.setWishCount(res['quantity']);
        this.setWishElemColor(res['quantity']);
    }
    deselectProduct(el, res) {
        let itemIconElem = el.querySelector('i');
        itemIconElem.classList.remove(this.wishedClass);
        this.setWishCount(res['quantity']);
        this.setWishElemColor(res['quantity']);
    }
    increment(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.add(el, prodId);
        }
    }
    decrement(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.delete(el, prodId);
        }
    }
    add(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.addUrl, data)
            .then(res => {
                this.selectProduct(el, res);
            })
    }
    delete(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.deleteUrl, data)
            .then(res => {
                this.deselectProduct(el, res);
            })
    }
    setWishBy(el) {
        let itemIconElem = el.querySelector('i');
        if(!itemIconElem.classList.contains(this.wishedClass)) {
            this.increment(el);
        } else {
            this.decrement(el);
        }
    }
    toggle() {
        const el = event.target;
        this.setWishBy(el);
    }
}
const wish = new WishMamager({
    addUrl: '/shop/wish/add/',
    deleteUrl: '/shop/wish/delete/',
    wishSelector: '#wish-total i',
    wishCountSelector: '#wish-counter span',
    wishedClass: 'text-primary',
    animationClass: 'wished_scale',
})

class CompareMamager {
    constructor(options) {
        this.addUrl = currentCompanyAlias()+options.addUrl;
        this.deleteUrl = currentCompanyAlias()+options.deleteUrl;
        this.compareElem = document.querySelector(options.compareSelector);
        this.compareCountElem = document.querySelector(options.compareCountSelector);
        this.compareCount = parseIntOrZero(getInnerHtml(options.compareCountSelector));
        this.comparedClass = options.comparedClass;
        this.animationClass = options.animationClass;
        // this.compares = [];
        this.setup();
    }
    setup() {
        if (isExist(this.compareElem) && isExist(this.animationClass)) {
            this.compareElem.addEventListener('animationend', (ev) => {
                if (ev.animationName == this.animationClass) {
                    this.compareElem.classList.remove(this.animationClass);
                }
            });
        }
    }
    getProdId(el) {
        if (el.hasAttribute('data-prodid') && (parseIntOrZero(el.dataset.prodid) != 0)) {
            return el.dataset.prodid;
        }
        return null;
    }
    setCompareCount(count) {
        this.compareCountElem.innerHTML = (count == 0)? '' : count;
        this.compareCountElem.hiddenParentByСondition(count > 0);
    }
    setCompareElemColor(count) {
        if(count > 0) {
            if (!this.compareElem.classList.contains(this.comparedClass)) {
                this.compareElem.classList.add(this.comparedClass);
                if (isExist(this.animationClass)) {
                    this.compareElem.classList.add(this.animationClass);
                }
            } else {
                if (isExist(this.animationClass)) {
                    this.compareElem.classList.add(this.animationClass);
                }
            }
        }
        if(count == 0 && this.compareElem.classList.contains(this.comparedClass)) {
            this.compareElem.classList.remove(this.comparedClass);
            if (isExist(this.animationClass)) {
                this.compareElem.classList.add(this.animationClass);
            }
        }
    }
    selectProduct(el, res) {
        let itemIconElem = el.querySelector('i');
        itemIconElem.classList.add(this.comparedClass);
        this.setCompareCount(res['quantity']);
        this.setCompareElemColor(res['quantity']);
    }
    deselectProduct(el, res) {
        let itemIconElem = el.querySelector('i');
        itemIconElem.classList.remove(this.comparedClass);
        this.setCompareCount(res['quantity']);
        this.setCompareElemColor(res['quantity']);
    }
    increment(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.add(el, prodId);
        }
    }
    decrement(el) {
        let prodId = this.getProdId(el);
        if (prodId !== null) {
            this.delete(el, prodId);
        }
    }
    add(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.addUrl, data)
            .then(res => {
                this.selectProduct(el, res);
            })
    }
    delete(el, prodId) {
        const data = {
            id: prodId,
        }
        fetchAsync('POST', this.deleteUrl, data)
            .then(res => {
                this.deselectProduct(el, res);
            })
    }
    setCompareBy(el) {
        let itemIconElem = el.querySelector('i');
        if(!itemIconElem.classList.contains(this.comparedClass)) {
            this.increment(el);
        } else {
            this.decrement(el);
        }
    }
    toggle() {
        const el = event.target;
        this.setCompareBy(el);
    }
}
const compare = new CompareMamager({
    addUrl: '/shop/compare/add/',
    deleteUrl: '/shop/compare/delete/',
    compareSelector: '#compare-total i',
    compareCountSelector: '#compare-counter span',
    comparedClass: 'text-primary',
    animationClass: 'compared_scale',
})

class InputWatcher {
    constructor(options) {
        this.obserEvent = options.obserEvent;
        this.obserElements = document.querySelectorAll(options.obserElementsSelector);
        this.handler = options.handler;
        this.setup();
    }
    setup() {
        this.obserElements.forEach((el) => {
            el.addEventListener(this.obserEvent, this.checkEvent);
        });
    }
    checkEvent = () => {
        let tmpCounter = 0;
        this.obserElements.forEach((el) => {
            let value = el.value.trim();
            if (value != '') {
                tmpCounter += 1;
            }
        });
        this.handler(this.obserElements.length == tmpCounter)
    }   
}

class FilterWatcher {
    constructor(options) {
        this.obserEvent = options.obserEvent;
        this.obserElements = document.querySelectorAll(options.obserElementsSelector);
        this.applySelector = document.querySelector(options.applySelector);
        this.filters = [];
        this.setup();
    }
    setup() {
        this.obserElements.forEach((el) => {
            el.addEventListener(this.obserEvent, this.checkEvent);
        });
    }
    checkEvent = () => {
        this.obserElements.forEach((el) => {
            const filter = this.getFilter(el);
            if (el.checked) {
                if (!this.filters.includes(filter)) {
                    this.filters.push(filter);
                }
            } else {
                this.filters = this.filters.filter((v)=>v!=filter);
            }
        });
        if (this.filters.length > 0) {
            this.applySelector.classList.remove('invisibile');
        } else {
            this.applySelector.classList.add('invisibile');
        }
    }
    getFilter(el) {
        return `${el.dataset.attr}=${el.dataset.val}`
    }
    apply(clear=false) {
        let urlParts = window.location.href.split('?');
        if (urlParts.length > 1) {
            const searchParams = urlParts[1].split('&').filter((p)=>p.startsWith('full_name'))
            if (!clear && this.filters.length > 0) {
                const paramsStr = this.filters.concat(searchParams).join('&');
                window.location.href = urlParts[0] + '?' + paramsStr
            } else {
                this.filters = [];
                const paramsStr = (searchParams.length > 0)? '?' + searchParams.join('&') : '';
                window.location.href = urlParts[0] + paramsStr;
            }
        } else {
            const paramsStr = (this.filters.length > 0)? '?' + this.filters.join('&') : '';
            window.location.href = urlParts[0] + paramsStr;
        }
    }
}

class Search {
    constructor(options) {
        this.searchInputElement = document.querySelector(options.searchInputElementSelector);
        this.params = [];
    }
    getSearchParams() {
        let rawParams = this.searchInputElement.value.split(',')
        rawParams.forEach((param) => {
            if(param !== '') {
                this.params.push(`full_name=${param.trim()}`)
            }
        });
        return this.params;
    }
    apply() {
        let urlParts = window.location.href.split('?');
        const searchParams = this.getSearchParams()
        if (urlParts.length > 1) {
            const filterParams = urlParts[1].split('&').filter((p)=>!p.startsWith('full_name'));
            let paramsStr = filterParams.concat(searchParams).join('&');
            paramsStr = (paramsStr.length > 0)? '?' + paramsStr : '';
            window.location.href = urlParts[0] + paramsStr;
        } else {
            const paramsStr = (searchParams.length > 0)? '?' + searchParams.join('&') : '';
            window.location.href = urlParts[0] + paramsStr;
        }
    }
}

const search = new Search({
    searchInputElementSelector: '#search',
})

class LocalStorageManager {
    set(key, value) {
        localStorage.setItem(key, value);
    }
    get(key) {
        return localStorage.getItem(key);
    }
    delete(key) {
        localStorage.removeItem(key);
    }
    clear() {
        localStorage.clear();
    }
}
const storage = new LocalStorageManager()


/* ---------------------------------------------- */

const handlers = {
    onlyDigital: (event) => {
        var ASCIICode = (event.which) ? event.which : event.keyCode
        if (ASCIICode > 31 && (ASCIICode < 48 || ASCIICode > 57)) {
            event.returnValue = false;
        }
    },
    notZero: (event) => {
        setTimeout(() => {
            if (event.target.value.length <= 1) {
                if (event.target.value == 0) {
                    event.target.value = 1
                } 
            }
            event.target.dataset.quantity = event.target.value;
            cart.update(event.target, event.target.dataset.prodid, event.target.dataset.quantity);
        }, '1000');
    },
    changeProdQty: (event) => {
        setTimeout(() => {
            event.target.dataset.quantity = event.target.value;
            cart.update(event.target, event.target.dataset.prodid, event.target.dataset.quantity);
        }, '1000');
    },
    changeWidth: (event) => {
        const length = event.target.value.length
        if (length > 3 || length <= 6) {
            event.target.size = event.target.value.length
        } 
    }
}
function handle(event, vs=[]) {
    /* <input 
        onkeydown="handle(event, ['onlyDigital'])" 
        onkeyup="handle(event, ['notZero'])"
        oninput="handle(event, ['changeProdQty'])"> */
    vs.forEach(v => handlers[v](event));
}

function inputHandlers(handlers) {
    /* <input data-handlers="keydown:onlyDigital,changeWidth|keyup:notZero|input:changeProdQty"> */
    const elems = document.querySelectorAll('[data-handlers]');
    elems.forEach((el) => {
        const eventHandler = el.dataset.handlers.split('|');
        eventHandler.forEach((handler) => {
            const [evList, hlList] = handler.split(':');
            const evts = evList.split(',');
            evts.forEach((evt) => {
                const hdls = hlList.split(',');
                hdls.forEach((hdlName) => {
                    el.addEventListener(evt, handlers[hdlName]);
                })
            })
        })
    })
}
inputHandlers(handlers);

// class InputValidation {
//     constructor(options) {
//         this.obserElements = document.querySelectorAll(options.obserElementsSelector);
//         this.eventValidators = options.eventValidators;
//         this.setup();
//     }
//     setup() {
//         this.obserElements.forEach((el) => {
//             for (const [event, validators] of Object.entries(this.eventValidators)) {
//                 validators.forEach((v) => {
//                     el.addEventListener('keydown', this.handler);
//                 });
//             }
//         });
//     }
//     handler(event) {
//         event.returnValue = onlyOneToNine(event);
//     }
// }
// const inputValidators = new InputValidation({
//     obserElementsSelector: '.onlyDigitalNotZero',
//     eventValidators: {'keydown': [
//         () => { return false }
//     ]}
// })