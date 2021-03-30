<template>

  <v-card
    style="height: 100%"
  >
    <v-sheet class="pa-4 gradient-lighten lighten-2 d-flex flex-row">
      <v-text-field
        v-model="search"
        label="Search"
        dark
        flat
        solo-inverted
        hide-details
        clearable
        clear-icon="mdi-close-circle-outline"
      ></v-text-field>
      <v-btn icon  class="mt-2 ml-2" @click="creatingDialog=!creatingDialog">
        <v-icon large>mdi-plus-circle-outline</v-icon>
      </v-btn>
    </v-sheet>
    <v-card-text>
      <v-responsive class="overflow-y-auto" max-height="75vh">
        <draggable
          :list="buttons"
          :group="{ name: group, pull: 'clone', put: false }"
        >
          <v-row
            v-for="(button, idx) in buttons"
            :key="idx"
          >
            <v-col cols="9">
              <v-chip style="width: 100%">
                {{button.default_text}}
              </v-chip>
            </v-col>
            <v-col cols="1">
              <v-btn icon @click="updateButtonId=button.id; updatingDialog=!updatingDialog;">
                <v-icon>mdi-pencil</v-icon>
              </v-btn>
            </v-col>
            <v-col cols="1">
              <v-btn icon @click="removeButtonId=button.id; removingDialog=!removingDialog;">
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </v-col>
          </v-row>
        </draggable>
      </v-responsive>
    </v-card-text>
<!--    Removing dialog-->
    <v-dialog
      v-model="removingDialog"
      persistent
      max-width="290"
    >
      <v-card>
        <v-card-title class="headline">
           Удаление Button
        </v-card-title>
        <v-card-text>Вы уверены?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="red darken-1"
            text
            @click="removingDialog = false; removeButton()"
          >
            Да
          </v-btn>
          <v-btn
            color="green darken-1"
            text
            @click="removingDialog = false"
          >
            Нет
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
<!--    Creating dialog-->
    <v-dialog
        v-model="creatingDialog"
        max-width="500px"
      >
        <v-card>
          <v-card-title>
            Добавить Button
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="newButtonText" label="Button default Text"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="creatingDialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="success"
              text
              @click="createNewButton"
            >
              Create
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
<!--    Updating dialog-->
      <v-dialog
          v-model="updatingDialog"
          max-width="500px"
        >
        <v-card>
          <v-card-title>
            Добавить Button
          </v-card-title>
          <v-card-text>
            <v-text-field v-model="updateButtonText" label="Insert new button text"></v-text-field>
          </v-card-text>
          <v-card-actions>
            <v-btn
              color="primary"
              text
              @click="updatingDialog = false"
            >
              Close
            </v-btn>
            <v-btn
              color="warning"
              text
              @click="updateButton"
            >
              Update
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  </v-card>
</template>

<script>
    export default {
      props: {
        buttons: Array,
        group: String
      },
      data: () => ({
        search: null,

        creatingDialog: false,
        newButtonText: null,

        updatingDialog: false,
        updateButtonId: null,
        updateButtonText: null,

        removingDialog: false,
        removeButtonId: null
      }),
      methods: {
        createNewButton () {
          this.$axios.post(
            '/quiz/buttons/',
            {
              default_text: this.newButtonText
            }
          )
            .then(response => {
              this.newButtonText = null
              this.$store.dispatch("components/setButtons")
            })

          this.creatingDialog = false
        },
        removeButton () {
          this.$axios.delete(
            "/quiz/buttons/" + this.removeButtonId
          )
          .then(response => {
            this.$store.dispatch("components/setButtons")
          })
        },
        updateButton () {
          this.$axios.put(
            "/quiz/buttons/" + this.updateButtonId + "/",
            {
              default_text: this.updateButtonText
            }
          )
          .then(response => {
            this.updateButtonId = null
            this.updateButtonText = null
            this.$store.dispatch("components/setButtons")
          })
          this.updatingDialog = false
        }
      }
  }
</script>

<style scoped>

</style>
