import OrgChart from './js/vendor/orgchart-webcomponents.js';

document.addEventListener('DOMContentLoaded', () => {
    let baseUrl = 'http://localhost:9999';
    let entryURL = `${baseUrl}/orgchart/entourage/`;
    let ajaxURLs = {
        'children': `${baseUrl}/orgchart/children/`,
        'parent': `${baseUrl}/orgchart/parent/`,
        'siblings': `${baseUrl}/orgchart/siblings/`,
        'families': `${baseUrl}/orgchart/family/`
    };
    let options = {
        'ajaxURL': ajaxURLs,
        'nodeContent': 'title',
        'nodeId': 'name',
        'draggable': true,
        'pan': true,
        'zoom': true
    };
    document.querySelector('#search').addEventListener('submit', (e) => {
        e.preventDefault();
        let value = document.querySelector('#search-text').value;
        console.log(value);
        options.data = entryURL + value;
        let orgchart = new OrgChart(options);
        let container = document.querySelector('#chart-container');
        container.innerHTML = '';
        container.appendChild(orgchart);
        return false;
    });

});