<template>
    <b-sidebar id="menu" title="Options" header-class="bg-dark d-flex" bg-variant="dark" text-variant="white"
        backdrop-variant="dark" body-class="pb-2" width="360px" backdrop>
        <b-row class="gap-1 mt-1 mb-2">
            <BuyMeCoffee></BuyMeCoffee>
            <b-btn to="/feedback" class="flex-grow-1" variant="primary">Give Feedback</b-btn>
        </b-row>
        <MenuTextOptions />
        <MenuObservations />
        <MenuQuestions />
        <MenuApplications />
    </b-sidebar>
</template>
<script>
import MenuObservations from './MenuObservations.vue'
import MenuTextOptions from './MenuTextOptions.vue'
import MenuQuestions from './MenuQuestions.vue'
import MenuApplications from './MenuApplications.vue'
export default {
    components: {
        MenuObservations,
        MenuTextOptions,
        MenuQuestions,
        MenuApplications
    }
}
</script>