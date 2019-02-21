$(function () {
    $('#datetimepicker1').datetimepicker({
        format: 'MM/DD/YYYY',
        defaultDate: new Date()
    });
});

var clientIdToName = {};
var productAreaIdToName = {};

function Feature(data) {
    this.feature_id = ko.observable(data.id);
    this.title = ko.observable(data.title);
    this.description = ko.observable(data.description);
    this.client_priority = ko.observable(data.client_priority);
    this.client_id = ko.observable(data.client_id);
    this.client_name = ko.observable(clientIdToName[data.client_id]);
    this.product_area_id = ko.observable(data.product_area_id);
    this.product_area_name = ko.observable(productAreaIdToName[data.product_area_id]);
    this.target_date = ko.observable(moment.utc(data.target_date, 'ddd, DD MMM YYYY HH:mm:ss GMT').format("MM/DD/YYYY"));

}

function Client(data) {
    this.client_id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}

function ProductArea(data) {
    this.product_area_id = ko.observable(data.id);
    this.name = ko.observable(data.name);
}


function TaskListViewModel() {
    // Data
    var self = this;
    self.features = ko.observableArray([]);
    self.clients = ko.observableArray([]);
    self.productareas = ko.observableArray([]);

    self.newFeatureTitleText = ko.observable();
    self.newFeatureDescriptionText = ko.observable();
    self.newFeatureClientPriorityText = ko.observable();
    self.newFeatureClientValue = ko.observable(self.clients[0]);
    self.newFeatureProductAreaValue = ko.observable(self.productareas[0]);
    self.newFeatureProductAreaText = ko.observable();
    self.newFeatureTargetDate = ko.observable();


    self.addFeature = function () {

        $('#addButton').prop('disabled', true);
        d = $("#datetimepicker1").find("input").val();

        new_feature = new Feature({
            title: this.newFeatureTitleText(),
            description: this.newFeatureDescriptionText(),
            client_priority: this.newFeatureClientPriorityText(),
            client_id: this.newFeatureClientValue().client_id(),
            product_area_id: this.newFeatureProductAreaValue().product_area_id(),
            target_date: this.newFeatureTargetDate()
            //target_date: "02/27/2019"
        });

        console.log(new_feature);

        // send update to server
        var plainFeature = {
            title: this.newFeatureTitleText(),
            description: self.newFeatureDescriptionText(),
            client_priority: this.newFeatureClientPriorityText(),
            client_id: this.newFeatureClientValue().client_id(),
            product_area_id: this.newFeatureProductAreaValue().product_area_id(),
            target_date: d
        };

        stringToSend = JSON.stringify(plainFeature);
        $.post("/api/add_feature", stringToSend, function (returnedData) {
            console.log("returnedData: " + returnedData);
            retObj = JSON.parse(returnedData);
            new_feature.feature_id = retObj.id;
            self.features.push(new_feature);
            $('#addButton').prop('disabled', false);
        })

        self.newFeatureTitleText("");
        self.newFeatureDescriptionText("");
        self.newFeatureClientPriorityText(1);
        self.newFeatureProductAreaText(1);

        self.loadModel();
    };

    self.removeFeature = function (feature) {
        idToRemove = feature.feature_id();
        strToSend = "/api/delete_feature/" + idToRemove;
        $.get(strToSend);
        self.loadModel();
    };

    self.loadModel = function () {
        // Load initial state from server, convert it to Client instances, then populate self.clients
        $.getJSON("/api/clients", function (allData) {
            var mappedClients = $.map(allData, function (item) {
                return new Client(item)
            });
            for (var i = 0; i < mappedClients.length; i++) {
                clientIdToName[mappedClients[i].client_id()] = mappedClients[i].name();
            }
            self.clients(mappedClients);
            // Load initial state from server, convert it to ProductArea instances, then populate self.productareas
            $.getJSON("/api/productareas", function (allData) {
                var mappedProductArea = $.map(allData, function (item) {
                    return new ProductArea(item)
                });
                for (var i = 0; i < mappedProductArea.length; i++) {
                    productAreaIdToName[mappedProductArea[i].product_area_id()] = mappedProductArea[i].name();
                }
                self.productareas(mappedProductArea);
                // Load initial state from server, convert it to Task instances, then populate self.tasks
                $.getJSON("/api/features", function (allData) {
                    var mappedFeatures = $.map(allData, function (item) {
                        return new Feature(item)
                    });
                    self.features(mappedFeatures);
                });
            });
        });
    };

    self.loadModel();
}

ko.applyBindings(new TaskListViewModel());
